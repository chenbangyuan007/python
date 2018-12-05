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
    country = dao.selectAll("select * from games", None)
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
    teamName = request.args.get('teamName')
    firstTeamId=request.args.get('firstTeamId')
    teams = []
    if teamName==None or teamName=='':
        return jsonify(teams)

    parameter=()
    sql="select t.id,t.name from team t  where 1=1 and "
    if teamName!=None:
        sql =sql +" t.`name` like %s"
        parameter=parameter+("%"+teamName+"%",)
    if firstTeamId!=None:
        sql =sql +" and t.id!=%s"
        parameter=parameter+(firstTeamId,)
    sql=sql+" group by t.id"
    teams=dao.selectAll(sql,parameter)
    return jsonify(teams)

@app.route('/findKeTeam')
def findKeTeam():
    firstTeamId=request.args.get('firstTeamId')
    parameter=(firstTeamId,)
    sql="select t.id,t.name from team t left join game_data gd on gd.second_team_id=t.id where gd.first_team_id=%s group by t.id"
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

@app.route('/syscBisaiData')
def syscBisaiData():
    countryId=request.args.get('countryId')
    gamesId=request.args.get('gamesId')
    year=request.args.get('year')
    pirod=dao.selectAll("select years,bsid,lv,lv1 from game_pirod where game_id=%s and name=%s and years=%s order by bsid asc",(countryId,gamesId,year))
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
    queryData = []
    parameter = (firstTeam, secondTeam)
    dataSql = "SELECT d.bisai_id,DATE_FORMAT(d.bs_time,'%Y-%m-%d %H:%i'), (select name from team where id=d.first_team_id) as '主队'," \
              " (select name from team where id=d.second_team_id) as '客队', d.full_score, d.full_concede, d.full_bigsmall, d.half_score," \
              " d.half_concede, d.half_bigsmall, p.bocaiGs, p.first_zhudui, p.first_pankou, p.first_cidui, p.finally_zhudui, p.finally_pankou, p.finally_cidui,p.pankouName"
    fromSql = " FROM game_data d LEFT JOIN pankou p ON d.bisai_id = p.bisaiId WHERE " \
              "d.first_team_id = %s AND d.second_team_id = %s ";
    if begin != None and begin != '':
        fromSql = fromSql + " AND d.bs_time BETWEEN %s AND %s "
        parameter = parameter + (begin, end)
    fromSql = fromSql + " AND ( p.bocaiGs = '澳门' OR p.bocaiGs = '易胜博' ) ORDER BY d.bs_time DESC"
    countSql = "select count(d.bisai_id)" + fromSql
    total = dao.selectAll(countSql, parameter)
    dataSql = dataSql + fromSql + " limit %s,%s"
    parameter = parameter + (fromData, limit)
    queryData = dao.selectAll(dataSql, parameter)
    result = {"data": queryData, "total": total[0][0]}
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.3.89', port=8089)
