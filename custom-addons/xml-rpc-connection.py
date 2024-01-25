import xmlrpc.client

url = "http://localhost:8069"
username = "odoo"
password = "odoo"
db = "db"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
# print(common.version())
user_uid = common.authenticate(db, username, password, {})
# print(user_uid)

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# search function
property_ids = models.execute_kw(
    db, user_uid, password, "estate.property", "search", [[]], {"offset": 1, "limit": 1}
)
print("search function ==>", property_ids)

# count function
count_property_ids = models.execute_kw(
    db, user_uid, password, "estate.property", "search_count", [[]]
)
print("count function ==>", count_property_ids)

# read function
read_property_ids = models.execute_kw(
    db,
    user_uid,
    password,
    "estate.property",
    "read",
    [property_ids],
    {"fields": ["name"]},
)
print("read function ==>", read_property_ids)

# search and read function
search_read_property_ids = models.execute_kw(
    db,
    user_uid,
    password,
    "estate.property",
    "search_read",
    [[]],
    {"fields": ["name"], "limit": 5},
)
print("search_read function ==>", search_read_property_ids)

# create function
create_property_id = models.execute_kw(
    db,
    user_uid,
    password,
    "estate.property",
    "create",
    [
        {
            "name": "New Property from RPC",
            "description": "New Property Description",
            "sales_id": user_uid,
        }
    ],
)
print("create function ==>", create_property_id)

# write function
write_property_id = models.execute_kw(
    db,
    user_uid,
    password,
    "estate.property",
    "write",
    [[create_property_id], {"name": "New Property from RPC - Updated"}],
)
read_name_get = models.execute_kw(
    db, user_uid, password, "estate.property", "name_get", [[create_property_id]]
)
print("write function ==>", read_name_get)

# unlink function
unlink_property_id = models.execute_kw(
    db, user_uid, password, "estate.property", "unlink", [[create_property_id]]
)
print("unlink function ==>", unlink_property_id)
