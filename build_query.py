def insert_query(table,names,values):

	if len(names)!=len(values):
		return None

	qur= " INSERT INTO "+table+"("
	i=0;
	ln = len(names)-1
	for name in names:
		if i<ln:
			qur = qur +name+","
		else:
			qur = qur +name+")"

		i=i+1

	qur= qur+" VALUES("
	i=0;
	ln = len(values)-1
	for value in values:
		if i<ln:
			qur = qur +"'"+value+"',"
		else:
			qur = qur +"'"+value+"') "

		i=i+1

	return qur

def update_query(table,names,values, where_stetment):

	if len(names)!=len(values):
		return None

	qur= " UPDATE "+table+" SET "
	i=0;
	ln = len(names)-1
	for name in names:
		if i<ln:
			qur = qur +name+" = "+"'"+values[i]+"', "
		else:
			qur = qur +name+" = "+"'"+values[i]+"' "
		i=i+1

	qur= qur+" WHERE "+where_stetment


	return qur

def select_query(table,column,where_stetment):

	qur = ""

	if len(column)>0:
		qur = "SELECT "+column+" FROM "
	else:
		qur = "SELECT * FROM "

	if len(where_stetment) > 0:
		qur = qur + table+" where "+where_stetment
	else:
		qur = qur + table
	
	return qur

	
