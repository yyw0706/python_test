# @Auther   :Mateo
# coding = utf-8

from MySQLManager import *

mysql_manager = MySQL_Manager("192.168.100.114", 3306, "Hero", "root", "123456")

# 创建表
create_sql = "create table hero(id int auto_increment primary key,name varchar(20) not null unique,skill varchar(20) not null) engine=innodb default charset=utf8;"
mysql_manager.create_table(create_sql)

# 添加数据
insert_sql = "insert into hero(id,name,skill) values(1,'李白','青莲剑歌');"
mysql_manager.insert(insert_sql)

# 查询语句
select_sql = "select * from hero;"
list = mysql_manager.select_all(select_sql)
print(list)

# 修改
update_sql = "update hero set name='韩信' where id=1;"
mysql_manager.update(update_sql)

# 删除语句
delete_sql = "delete from hero where id=1;"
mysql_manager.delete(delete_sql)

