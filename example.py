import confluence.connector as c

con = c.Confluence('admin','admin')
con.set_serverurl('http://lasnq2018-d6-linux:1990/confluence/')
print(con.get_serverurl())