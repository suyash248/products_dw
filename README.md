# Products

### Requirements
Python 3.x, pip3, MySQL

### How to run?

1. Move to ```<project-dir>```, create virual environment and then activate it as

```sh
$ cd <project-dir>
$ virtualenv .environment
$ source .environment/bin/activate
```

2. Edit configuration under ```settings.py```. i.e. provide configuration/settings related to DB and other constants.

> If you are using PyCharm then environment variables can be specified under `run configuration`, or env variables can
also be defined under <virtualenv>/bin/activate file.

```sh
export PG_DB_NAME=<db_name>
export PG_DB_HOST=<db_host>
export PG_DB_USER=<db_user>
export PG_DB_PASSWORD=<db_password>
export PG_DB_PORT=<db_port>
```

3. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

4. Under ```<project-dir>``` install requirements/dependencies as 

```sh 
$ pip3 install -r requirements.txt
```

5. Run DB migrations defined under `migrations/v1.sql`, it will create tables `products`, `categories` 
and creates a few categories records.

6. Run server as - 
```sh
$ python app.py 
```
> Now you can access the application by visiting ```{protocol}://{host}:{port}```. For localhost it is ```http://localhost:5000```.


### Applications & Endpoints

There are following three APIs -

#### 1. Adding a new product - 

> POST ```{host}:{port}/api/v1/products```.

*Request body*

```javascript
{
	"brand": "b9834",
	"title": "title9837",
	"description": "description90548",
	"sku": "sku9494",
  	"category": "a572aae1-8b8c-4a8d-a17d-4655b8487960", # category id
  	"prod_type": "prodtype405",
  	"mrp": 220,
  	"available_price": 205
}
```

*Response*

```javascript
{
    "success": true,
    "message": "Product added successfully!",
    "data": null,
    "errors": []
}
```

#### 2. Update product - 

> PUT ```{host}:{port}/api/v1/products/<product_id>```.

*Request body*

```javascript
{
	"brand": "b7",
	"title": "title12updated",
	"description": "description12upd",
	"sku": "sku12",
  	"category": "a572aae1-8b8c-4a8d-a17d-4655b8487960",
  	"prod_type": "prodtype12",
  	"mrp": 84
}
```

*Response*

```javascript
{
    "success": true,
    "message": "Product updated successfully!",
    "data": null,
    "errors": []
}
```

#### 3. Get all products(paginated) - 

> POST ```{host}:{port}/api/v1/products/filter?page=1&per_page=10```.

*Request body*

```javascript
{
	"filter_by": {
		# WHERE condition1 AND condition2 AND......AND conditionN
		"and": [ 
			{
				"field_name": "Product.title",  # Model.field
				"operator": "contains",
				"field_value": "1"
			},
			{
				"field_name": "Category.name",
				"operator": "eq",
				"field_value": "Android"
			}
		],
		# WHERE condition1 OR condition2 OR......OR conditionN
		"or": [
			{
				"field_name": "Product.sku",
				"operator": "contains",
				"field_value": "1"
			}
		]
	},
	"order_by": ["-Product.created_at"] .   # ORDER BY products.created_at DESC.
}
```
 > Operators - `equals, eq, ==, =`, `not_equals, ne, !=, ~=`, `less_than, lt, <`, `less_than_equals, lte, <=`,
`greater_than, gt, >`, `greater_than_equals, gte, >=`, `like, ilike`, `startswith, istartswith, endswith, iendswith`, 
`contains, icontains`, `in, notin`, `isnull, isnotnull`,

*Response*

```javascript
{
    "success": true,
    "message": "",
    "data": [
        {
            "product_id": "eb40f166-347b-42f8-94a6-351742e58342",
            "title": "title9837",
            "brand": "b9834",
            "description": "description90548",
            "sku": "sku9494",
            "category": "a572aae1-8b8c-4a8d-a17d-4655b8487960",
            "product_created_at": "2019-01-02T08:15:13.846546",
            "product_updated_at": "2019-01-02T08:15:13.846550",
            "category_name": "Android",
            "super_category": "e92fa102-9c79-44ec-b36c-35f0f3c63b26"
        },
        .....
        .....
     }
}
```

#### 4. Get a products' count in each discount range - 

> GET ```{host}:{port}/api/v1/products/discounts```.

*Response*

```javascript
{
    "success": true,
    "message": "",
    "data": {
        "10-30%": 3,
        "0-10%": 3,
        "0%": 2,
        "30-50%": 3,
        ">50": 2
    },
    "errors": []
}
```


#### 5. Get all products(paginated) - 

> GET ```{host}:{port}/api/v1/api/v1/products?page=1&per_page=5```.

*Response*

```javascript
{
    "success": true,
    "message": "",
    "data": [
        {
            "product_id": "eb40f166-347b-42f8-94a6-351742e58342",
            "title": "title9837",
            "brand": "b9834",
            "description": "description90548",
            "sku": "sku9494",
            "category": "a572aae1-8b8c-4a8d-a17d-4655b8487960",
            "product_created_at": "2019-01-02T08:15:13.846546",
            "product_updated_at": "2019-01-02T08:15:13.846550",
            "category_name": "Android",
            "super_category": "e92fa102-9c79-44ec-b36c-35f0f3c63b26"
        },
        .....
        .....
     }
}
```

#### 6. Get a product by id - 

> GET ```{host}:{port}/api/v1/api/v1/products/<product_id>```.

*Response*

```javascript
{
    "success": true,
    "message": "",
    "data": [
        {
            "product_id": "eb40f166-347b-42f8-94a6-351742e58342",
            "title": "title9837",
            "brand": "b9834",
            "description": "description90548",
            "sku": "sku9494",
            "category": "a572aae1-8b8c-4a8d-a17d-4655b8487960",
            "product_created_at": "2019-01-02T08:15:13.846546",
            "product_updated_at": "2019-01-02T08:15:13.846550",
            "category_name": "Android",
            "super_category": "e92fa102-9c79-44ec-b36c-35f0f3c63b26"
        }
     }
}
```

### Error format - 

```javascript
{
    "success": false,
    "message": "<error_msg>",
    "data": null,
    "errors": [
        {
            "error_constant": "SOME_ERROR_CONSTANT", # BAD_REQUEST, AUTH_FAILED, REQUIRED_FIELD etc.
            "message": "<error_stacktrace>"
        }
    ]
}
```
e.g. -

```javascript
{
    "success": false,
    "message": "Database error occurred - syntax error at or near \"test\"",
    "data": null,
    "errors": [
        {
            "error_constant": "DB_ERROR",
            "message": "syntax error at or near \"test\"\nLINE 1: ...1%'  ORDER BY products.created_at desc LIMIT 50 OFFSET"
        }
    ]
}
```

### Links -
 - [Postmant API dump](https://github.com/suyash248/products_dw/blob/master/Products_Dw.postman_collection.json)

### TODO - 
1. Unit test cases.
2. Use a wsgi server like Gunicorn.
3. Centralized logging.
4. DB migrations(like alembic).
