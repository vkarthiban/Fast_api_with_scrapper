from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import manage_db as db_con
from pydantic import BaseModel

class User(BaseModel):
    name: str
    mobile: str | None = None
    email: str | None = None
 
app = FastAPI()

@app.get("/")
async def get_users():
    try:
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()
        response_data = []
        for row in rows:
            response_data.append({"id": row[0], "name": row[1],"mobile": row[2],"email": row[3]})
        db_connection.close()
        return JSONResponse(content=response_data)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in get users function at %s:%s' % (exc_traceback.tb_lineno, e))  


@app.post("/user/create/")
async def create_user(user:User):
    try:
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO user (name, mobile, email, datamode, created_on, updated_on) VALUES ('{name}', '{mobile}', '{email}', 'active', NOW(), NOW());".format(name=user.name,mobile=user.mobile,email=user.email)
        res = cursor.execute(insert_query)
        db_connection.commit()
        db_connection.close()
        response_data = {'status':'sucess'}
        return JSONResponse(content=response_data)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in create table function at %s:%s' % (exc_traceback.tb_lineno, e)) 


@app.patch("/user/update/{user_id}",response_model=User)
async def update_user(user_id:str,user:User):
    try:
        update_query = 'UPDATE user set  '
        for Usr in user:
            update_query += str(Usr[0]) + " = '" + str(Usr[1]) + "' , "
        update_query += "updated_on = NOW() WHERE id = {user_id};".format(user_id=user_id)
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        res = cursor.execute(update_query)
        db_connection.commit()
        db_connection.close()
        response_data = {'status':'User updated Sucessfully'}
        return JSONResponse(content=response_data)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in update table function at %s:%s' % (exc_traceback.tb_lineno, e))  

@app.get("/user/deactive/{user_id}")
async def deactive_user(user_id:str):
    try:
        update_query = "UPDATE user set datamode = 'inactive' WHERE id = {user_id};".format(user_id=user_id)
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        res = cursor.execute(update_query)
        db_connection.commit()
        db_connection.close()
        response_data = {'status':'User deactived Sucessfully'}
        return JSONResponse(content=response_data)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in update table function at %s:%s' % (exc_traceback.tb_lineno, e))  

@app.delete("/user/delete/{user_id}")
async def delete_user(user_id:str):
    try:
        delete_query = "DELETE FROM user WHERE id={user_id};".format(user_id=user_id)
        db_connection = db_con.connection_pool()
        cursor = db_connection.cursor()
        res = cursor.execute(delete_query)
        db_connection.commit()
        db_connection.close()
        response_data = {'status':'User delete Sucessfully'}
        return JSONResponse(content=response_data)
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        print('Error in delete table function at %s:%s' % (exc_traceback.tb_lineno, e))          


