__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from util.error_handlers.exceptions.exceptions import ExceptionBuilder, DatabaseException
from util.constants.error_codes import ErrorCode
from util.commons import Column

class OperatorEvaluator(object):
    """Represents an operator"""
    def __init__(self, model_cls, field_name, field_value):
        self.model_cls = model_cls
        self.field_name = field_name
        self.field_value = field_value

    @staticmethod
    def obj(operator_name, model_cls, field_name, field_value):
        operator_name = operator_name.lower()
        try:
            op_eval_cls = __OPERATORS_MAPPING__[operator_name]
            return op_eval_cls(model_cls, field_name, field_value)
        except:
            ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_OPERATOR, operator_name,
                    message="Invalid operator: {}".format(operator_name)).throw()

    def expr(self):
        """Evaluates criterion and returns expression to be used inside `model_cls.query.filter(*expressions)` method.
        Concrete operator classes must override this method."""
        ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_OPERATOR, self.field_name,
                    message="Invalid operator").throw()

    @property
    def model_field(self) -> Column:
        try:
            return getattr(self.model_cls, self.field_name)
        except:
            ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_FIELD, self.field_name,
                message="Couldn't find {} under {}".format(self.field_name, self.model_cls.__name__)).throw()

class __Equals__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='=', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __NotEquals__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='!=', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __LessThan__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='<', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __LessThanEq__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='<=', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __GreaterThan__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='>', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __GreaterThanEq__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='>=', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __IN__(OperatorEvaluator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()

        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%(({col_name}))s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='IN', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __NotIn__(OperatorEvaluator):
    def expr(self):
        try:
            iter(self.field_value)
        except TypeError as te:
            ExceptionBuilder(DatabaseException).error(ErrorCode.INVALID_DATA_TYPE, self.field_name,
                            message="field_value must be iterable").throw()
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%(({col_name}))s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='NOT IN', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value}

class __IsNull__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        whereclause_criterion = "{col_name} {operator}".format(
            col_name=col_name, operator='IS NULL'
        )
        return whereclause_criterion, {}

class __IsNotNull__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        whereclause_criterion = "{col_name} {operator}".format(
            col_name=col_name, operator='NOTNULL'
        )
        return whereclause_criterion, {}

class __Like__(OperatorEvaluator):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='LIKE', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: '%'+self.field_value+'%'}

class __StartsWith__(__Like__):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='LIKE', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: self.field_value + '%'}

class __EndsWith__(__Like__):
    def expr(self):
        col_name = "{table}.{col_name}".format(table=self.model_cls.__tablename__, col_name=self.model_field.name)
        col_value_placeholder = "%({col_name})s".format(col_name=col_name)
        whereclause_criterion = "{col_name} {operator} {col_value_placeholder}".format(
            col_name=col_name, operator='LIKE', col_value_placeholder=col_value_placeholder
        )
        return whereclause_criterion, {col_name: '%' + self.field_value}

class __Contains__(__Like__):
    def expr(self):
        return super(__Contains__, self).expr()

# Maps `operator_name` to corresponding 'operator` class.
__OPERATORS_MAPPING__ = {
    'equals': __Equals__,
    'eq': __Equals__,
    '==': __Equals__,

    'notequals': __NotEquals__,
    'not_equals': __NotEquals__,
    'ne': __NotEquals__,
    '!=': __NotEquals__,
    '~=': __NotEquals__,

    'less_than': __LessThan__,
    'lt': __LessThan__,
    '<': __LessThan__,

    'less_than_equals': __LessThanEq__,
    'lte': __LessThanEq__,
    '<=': __LessThanEq__,

    'greater_than': __GreaterThan__,
    'gt': __GreaterThan__,
    '>': __GreaterThan__,

    'greater_than_equals': __GreaterThanEq__,
    'gte': __GreaterThanEq__,
    '>=': __GreaterThanEq__,

    'like': __Like__,
    'startswith': __StartsWith__,
    'endswith': __EndsWith__,
    'contains': __Contains__,

    'in': __IN__,
    'notin': __NotIn__,

    'isnull': __IsNull__,
    'isnotnull': __IsNotNull__
}