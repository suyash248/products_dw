__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from psycopg2.extras import RealDictCursor
from models import BaseModel
from util.commons import Column, load_class
from util.constants.error_codes import ErrorCode
from util.error_handlers.exceptions import ExceptionBuilder, DatabaseException
from util.logger import Logger
from util.query.criterion import Criterion

# TODO - Has to move this under config.
model_module = 'models'

class __JoinClause__(object):
    def __init__(self, right_model_cls, left_model_field, right_model_field, right_model_cls_label=None, type='LEFT'):
        self.right_model_cls = right_model_cls
        self.right_model_field = right_model_field
        self.left_model_field = left_model_field
        self.right_model_cls_label = right_model_cls_label
        self.type = type

class Query(object):
    def __init__(self):
        self.query = ""
        self.tablename = ""
        self.select_clause = ""
        self.where_clause = ""
        self.order_by_clause = ""
        self.joins = []
        self.and_where_clause = []
        self.or_where_clause = []
        self.query_params = {}

    @staticmethod
    def select(*model_fields_or_classes):
        model_fields = []
        for model_field in model_fields_or_classes:
            if isinstance(model_field, (BaseModel,)):
                model_fields.append(model_field.fields())
            elif isinstance(model_field, (Column,)):
                model_fields.append(model_field)
            else:
                Logger.error("Unknown field type: {}: {}".format(model_field, type(model_field)))

        col_names = []
        for mf_col in model_fields:
            if mf_col._label: col_name = '{table}.{col} AS {label}'.format(
                table=mf_col.tablename, col=mf_col.name, label=mf_col._label)
            else: col_name = mf_col.name
            col_names.append(col_name)
        select_clause = ", ".join(col_names)

        _self = Query()
        _self.select_clause = select_clause
        return _self

    def from_table(self, model_cls):
        if issubclass(model_cls, (BaseModel,)):
            self.tablename = model_cls.__tablename__
        else: Logger.error("Unknown model/table type: {}: {}".format(model_cls, type(model_cls)))
        return self

    def __eval_criterion__(self, field_name, field_value, operator):
        m_cls_name = field_name[:field_name.rindex('.')]
        field_name = field_name[field_name.rindex('.')+1:]
        m_cls = load_class('{}.{}'.format(model_module,  m_cls_name))

        criterion = Criterion(m_cls, field_name, field_value, operator)
        return criterion.eval()

    def __eval_criteria__(self, criteria=()):
        expressions = []
        error_fields = []
        if not isinstance(criteria, (list, tuple, set)): criteria = [criteria]
        for criterion in criteria:
            try:
                evaluated_criterion, query_params = self.__eval_criterion__(criterion.get('field_name'), criterion.get('field_value'),
                                                              criterion.get('operator'))
                self.query_params.update(query_params)
                expressions.append(evaluated_criterion)
            except AttributeError as ae:
                error_fields.append(criterion.get('field_name', 'unknown'))
        if len(error_fields) > 0:
            ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_FIELD, *error_fields).throw()
        return expressions

    def where(self, and_criteria=(), or_criteria=()):
        self.and_where_clause.extend(self.__eval_criteria__(and_criteria))
        self.or_where_clause.extend(self.__eval_criteria__(or_criteria))
        return self

    def order_by(self, *ordering_fields):
        ordering_criteria = []
        for ordering_field in ordering_fields:
            direction = 'desc' if ordering_field.startswith('-') else 'asc'
            model_cls_field_name = ordering_field.replace('-', '', 1)
            m_cls_name = model_cls_field_name[:model_cls_field_name.rindex('.')]
            field_name = model_cls_field_name[model_cls_field_name.rindex('.') + 1:]
            m_cls = load_class('{}.{}'.format(model_module, m_cls_name))
            model_field = getattr(m_cls, field_name)
            ordering_criteria.append('{table}.{col_name} {direction}'.format(
                table=m_cls.__tablename__, col_name=model_field.name, direction=direction))

        if ordering_criteria:
            self.order_by_clause = ' ORDER BY {}'.format(', '.join(ordering_criteria))
        return self

    def slice(self, page=1, per_page=10):
        limit = per_page
        offset = limit * (page - 1)
        self.limit_clause = 'LIMIT {limit} OFFSET {offset}'.format(limit=limit, offset=offset)
        return self

    def leftjoin(self, right_model_cls, left_model_field, right_model_field, right_model_cls_label=None):
        # SELECT animal.ID, breed1.BreedName as BreedName1, breed2.BreadName as BreadName2
        # FROM animal
        #    LEFT JOIN breed as breed1 ON animal.breedID=breed1.ID
        #    LEFT JOIN breed as breed2 ON animal.breedID=breed2.ID
        # WHERE animal.ID='7';
        self.joins.append(__JoinClause__(right_model_cls, left_model_field, right_model_field,
                                         right_model_cls_label=right_model_cls_label, type='LEFT'))
        return self

    def build(self):
        """
        Constructs SQL-alchemy queryset via JSON.
        :return: SQL-alchemy queryset.
        """
        joinclause = []
        for jclause in self.joins:
            joinwith = jclause.right_model_cls.__tablename__
            if jclause.right_model_cls_label:
                joinwith += ' AS {} '.format(jclause.right_model_cls_label)
            joinclause.append(
                '{type} JOIN {joinwith} ON {left_tablename}.{left_col} = {right_tablename}.{right_col}'.format(
                    type='LEFT', joinwith=joinwith,
                    left_tablename=self.tablename, right_tablename=jclause.right_model_cls.__tablename__,
                    left_col=jclause.left_model_field.name, right_col=jclause.right_model_field.name
                )
            )
        joinclause = ' '.join(joinclause)

        if self.and_where_clause:
            self.where_clause += " WHERE " + "AND ".join(self.and_where_clause)
        if self.or_where_clause:
            self.where_clause += " OR " + "OR ".join(self.or_where_clause)

        self.query = """SELECT {select_clause} FROM {tablename} {joinclause} {where_clause} {order_by_clause} {limit_clause}""".format(
            select_clause=self.select_clause, tablename=self.tablename, joinclause=joinclause,
            where_clause=self.where_clause, order_by_clause=self.order_by_clause, limit_clause=self.limit_clause)

        Logger.info(self.query)
        return self

    def exec(self, pg_con, query_params={}, mapper=None):
        self.query_params.update(query_params)
        with pg_con:
            with pg_con.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(self.query, self.query_params)
                results = cur.fetchall()
                if mapper:
                    results = list(map(lambda row_dict: mapper(row_dict), results))
                return results