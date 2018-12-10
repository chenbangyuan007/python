from flask import Flask, jsonify, request
from flask import render_template
import dao;
import fechPankou
import games
import fetchGames
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/findCountry')
def hello():
    country = dao.selectAll("select id,country from games", None)
    return jsonify(country)


@app.route('/findGames/<countryId>')
def findGames(countryId):
    games = dao.selectAll("select id,name from game_pirod gp where game_id=%s group by name", (countryId,))
    return jsonify(games)


@app.route('/findYears/<countryId>')
def findYear(countryId):
    games = dao.selectAll("select id,years from game_pirod where game_id=%s", (countryId,))

    return jsonify(games)


@app.route('/findTeam')
def findTeam():
    gameId = request.args.get('gameId')
    countryId = request.args.get('countryId')
    sql ="select t.id,t.`name` from games g left join game_pirod p on p.game_id=g.id left join team t on t.game_id=p.bsid where 1=1 "
    parameter=()
    if countryId!=None:
        sql=sql+" and g.id=%s"
        parameter=parameter+(countryId,)
    if gameId!=None:
        sql=sql+" and p.name=%s"
        parameter=parameter+(gameId,)
    sql=sql+" and t.id is not null group by t.id"
    teams=dao.selectAll(sql,parameter)
    return jsonify(teams)

@app.route('/findKeTeam')
def findKeTeam():
    firstTeamId=request.args.get('firstTeamId')
    gameId = request.args.get('gameId')
    countryId = request.args.get('countryId')
    sql ="select t.id,t.`name` from games g left join game_pirod p on p.game_id=g.id left join team t on t.game_id=p.bsid where 1=1 "
    parameter=()
    if countryId!=None:
        sql=sql+" and g.id=%s"
        parameter=parameter+(countryId,)
    if gameId!=None:
        sql=sql+" and p.name=%s"
        parameter=parameter+(gameId,)
    if firstTeamId!=None:
        sql=sql+" and t.id!=%s"
        parameter=parameter+(firstTeamId,)
    sql=sql+" and t.id is not null group by t.id"
    teams=dao.selectAll(sql,parameter)
    return jsonify(teams)

@app.route('/syscPankou')
def syscPankou():
    firstTeamId=request.args.get('firstTeamId')
    secondTeamsId=request.args.get('secondTeamsId')
    parameter=(firstTeamId,secondTeamsId)
    sql="select gd.bisai_id from game_data gd where gd.first_team_id=%s and gd.second_team_id=%s"
    teams=dao.selectAll(sql,parameter)
    for i in range(len(teams)):
        fechPankou.fetchPankou(teams[i][0])
    return jsonify(("同步成功",))

@app.route('/syscBaseData')
def syscBaseData():
    games.fechCountry()
    return jsonify(("同步成功",))

@app.route('/findBocaiGsNames')
def findBocaiGsNames():
    data=dao.selectAll("select id,bocaiGsName from bocaiGs",None)
    return jsonify(data)

@app.route('/findPankouLabel')
def findPankouLabel():
    data=dao.selectAll("select id,pankou,alias from pankouLabel order by alias asc ",None)
    return jsonify(data)

@app.route('/syscBisaiData')
def syscBisaiData():
    countryId=request.args.get('countryId')
    gamesId=request.args.get('gamesId')
    year=request.args.get('year')
    pirod=None
    if year!=None or year!='undefined':
        pirod=dao.selectAll("select years,bsid,lv,lv1 from game_pirod where game_id=%s and name=%s and years=%s order by bsid asc",(countryId,gamesId,year))
    else:
        pirod=dao.selectAll("select years,bsid,lv,lv1 from game_pirod where game_id=%s and name=%s  order by bsid asc",(countryId,gamesId))
    for j in range(len(pirod)):
        year=pirod[j][0]
        game_id=pirod[j][1]
        lv=pirod[j][2]
        lv1=pirod[j][3]
        domine=None
        if lv==1 and lv1==0:
            domine='League'
        elif lv==1 and lv1==1:
            domine='SubLeague'
        elif lv==2 and lv1==0:
            domine='CupMatch'
        print(game_id,domine,year)
        fetchGames.fetchGames(game_id,domine,year)
    return jsonify(("同步成功",))

@app.route('/query/<page>/<pageSize>', methods=["POST"])
def query(page, pageSize):
    page =int(page)-1
    fromData = int(pageSize) * int(page)
    limit = int(pageSize)
    begin = request.form['begin']
    end = request.form['end']

    firstTeam = request.form['firstTeam']
    secondTeam = request.form['secondTeam']
    bocaiGs = request.form.getlist('bocaiGs[]')
    pankous = request.form.getlist('pankou[]')
    finally_pankou = request.form.getlist('finally_pankou[]')

    gameId = request.form['gameId']
    countryId = request.form['countryId']

    dataSql = "SELECT d.bisai_id,DATE_FORMAT(d.bs_time,'%Y-%m-%d %H:%i'), (select name from team where id=d.first_team_id) as '主队'," \
              " (select name from team where id=d.second_team_id) as '客队', d.full_score, d.full_concede, d.full_bigsmall, d.half_score," \
              " d.half_concede, d.half_bigsmall, p.bocaiGs, p.first_zhudui, p.first_pankou, p.first_cidui, p.finally_zhudui, p.finally_pankou, p.finally_cidui,p.pankouName,first_pankou_alias,finally_pankou_alias"
    fromSql = " FROM game_data d LEFT JOIN pankou p ON d.bisai_id = p.bisaiId WHERE 1=1"
    parameter=()
    if countryId!=None and countryId!='undefined':
        fromSql=fromSql+" and d.country_id = %s"
        parameter = parameter + (countryId, )
    if gameId!=None and gameId!='undefined':
        fromSql=fromSql+" and d.liansai = %s"
        parameter = parameter + (gameId, )
    if firstTeam!=None and firstTeam!='undefined':
       fromSql=fromSql+" and d.first_team_id = %s"
       parameter = parameter + (firstTeam, )
    if secondTeam!=None and secondTeam!='undefined':
        fromSql=fromSql+" and d.second_team_id = %s"
        parameter = parameter + (secondTeam, )
    if begin != None and begin != '':
        fromSql = fromSql + " AND d.bs_time BETWEEN %s AND %s "
        parameter = parameter + (begin, end)
    if bocaiGs!=None and len(bocaiGs)>0:
        bocaiNames="";
        for i in range(len(bocaiGs)):
            bocaiNames=bocaiNames+"'"+bocaiGs[i]+"'"
            if i<len(bocaiGs)-1:
                bocaiNames=bocaiNames+","
        fromSql = fromSql + " AND p.bocaiGs in ("+bocaiNames+") "
    if pankous!=None and len(pankous)>0:
        pankou="";
        for i in range(len(pankous)):
            pankou=pankou+"'"+pankous[i]+"'"
            if i<len(pankous)-1:
                pankou=pankou+","
        fromSql = fromSql + " AND p.first_pankou_alias in ("+pankou+") "

    if finally_pankou!=None and len(finally_pankou)>0:
        fin_pankou="";
        for i in range(len(finally_pankou)):
            fin_pankou=fin_pankou+"'"+finally_pankou[i]+"'"
            if i<len(finally_pankou)-1:
                fin_pankou=fin_pankou+","
        fromSql = fromSql + " AND p.finally_pankou_alias in ("+fin_pankou+") "
    fromSql=fromSql+" ORDER BY d.bs_time DESC"
    countSql = "select count(d.bisai_id)" + fromSql
    total = dao.selectAll(countSql, parameter)
    dataSql = dataSql + fromSql + " limit %s,%s"
    parameter = parameter + (fromData, limit)
    queryData = dao.selectAll(dataSql, parameter)
    result = {"data": queryData, "total": total[0][0]}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.3.89', port=8089)
