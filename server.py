
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,url_for

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://yl4111:2052@35.231.103.173:5432/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  #cursor = g.conn.execute("SELECT playerid,name FROM player")
  #names = []
  #for result in cursor:
  #  names.append(result)  # can also be accessed using result[0]
  #cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
#@app.route('/another')
#def another():
#  return render_template("another.html")

#page for teams
@app.route('/team')
def team():
  cursor = g.conn.execute("SELECT teamid,name,conference,division FROM team ORDER BY conference ASC,division ASC")
  names = []
  for result in cursor:
     names.append(result)  # can also be accessed using result[0]
  cursor.close()
  context=dict(data=names)
  return render_template("team.html",**context)


#teamhomepage
@app.route('/team/<int:teamid>')
def teaminfo(teamid):
  cursor = g.conn.execute("SELECT team.name AS name,arena,executive,conference,division,coach.name AS coach,coach.coachid as coachid  FROM team,coachof,coach WHERE team.teamid=%s AND team.teamid=coachof.teamid AND coach.coachid=coachof.coachid",teamid)
  teaminfo = []
  for result in cursor:
    teaminfo.append(result)  # can also be accessed using result[0]
  cursor.close()
  teamname=teaminfo[0].name
  return render_template("teaminfo.html",data=teaminfo,teamname=teamname,teamid=teamid)

@app.route('/team/<int:teamid>/roster')
def roster(teamid):
  cursor = g.conn.execute("SELECT player.name as name,team.name as tname,player.playerid as playerid,year FROM team,playerof,player WHERE team.teamid=%s AND player.playerid=playerof.playerid AND team.teamid=playerof.teamid",teamid)
  roster=[]
  for result in cursor:
    roster.append(result)
  cursor.close()
  teamname=roster[0].tname
  return render_template("roster.html",data=roster,teamname=teamname) 
 	 

@app.route('/player')
def servpage():
  return render_template("player.html")

@app.route('/player',methods=["GET","POST"])
def getdata():
  if request.method=="POST":
    playername=request.form['name']
  return redirect(url_for('playersearch',name=playername))


@app.route('/player/<name>')
def playersearch(name):
  thisname='%'+name+'%'
  cursor=g.conn.execute('SELECT player.playerid as playerid,player.name as pname,player.name as name,team.name as tname,team.teamid as teamid FROM player,team,playerof WHERE player.name like %s AND player.playerid=playerof.playerid AND team.teamid=playerof.teamid AND playerof.year=2019',thisname)
  playerresult=[]
  for result in cursor:
    playerresult.append(result)
  cursor.close()
  return render_template("playerresult.html",name=name,data=playerresult)



@app.route('/playerinfo/<int:playerid>')
def playerinfo(playerid):
  cursor=g.conn.execute('SELECT * FROM player WHERE playerid=%s',playerid)
  playerinfo=[]
  for result in cursor:
    playerinfo.append(result)
  cursor.close()
  cursor=g.conn.execute('SELECT a.gameid AS gameid,date,homename,awayname,minute,fg,fga,fgp,tpt,tpta,tptp,ft,fta,ftg,orb,drb,trb,ast,stl,blk,tov,psf,pts,plusminus FROM playerstat,(SELECT home.name AS homename,away.name AS awayname,gameid,date FROM team AS home,team AS away,game WHERE homeid=home.teamid AND awayid=away.teamid)AS a WHERE playerid=%s AND a.gameid=playerstat.gameid',playerid)
  playerstat=[]
  for result in cursor:
    playerstat.append(result)
  cursor.close()
  return render_template("playerinfo.html",playerinfo=playerinfo,data=playerstat)

@app.route('/playoff')
def playoff():
  cursor=g.conn.execute('SELECT * FROM playoff2019 ORDER BY round DESC,con DESC')
  playoff=[]
  for result in cursor:
    playoff.append(result)
  cursor.close()
  return render_template("playoff.html",playoff=playoff)

@app.route('/series/<int:serieid>')
def serie(serieid):
  cursor=g.conn.execute('select series.serieid,hasgame.gameid,homename,homeid,awayname,awayid,date,homepts,awaypts from teammatch,series,hasgame where series.serieid=%s and series.serieid=hasgame.serieid and hasgame.gameid=teammatch.gameid',serieid)
  match=[]
  for result in cursor:
    match.append(result)
  cursor.close()
  return render_template("series.html",data=match)

@app.route('/game/<int:gameid>')
def game(gameid):
  cursor=g.conn.execute('select team.teamid as teamid,team.name as name,game.gameid as gameid,fg,fga,fgp,tpt,tpta,tptp,ft,fta,ftp,orb,drb,trb,ast,stl,blk,tov,foul,pts,winloss from team,teamstat,game where game.gameid=teamstat.gameid and teamstat.teamid=team.teamid and team.teamid=game.homeid and game.gameid=%s',gameid)
  hometeam=[]
  for result in cursor:
    hometeam.append(result)
  cursor.close()
  cursor=g.conn.execute('select team.teamid as teamid,team.name as name,game.gameid as gameid,fg,fga,fgp,tpt,tpta,tptp,ft,fta,ftp,orb,drb,trb,ast,stl,blk,tov,foul,pts,winloss from team,teamstat,game where game.gameid=teamstat.gameid and teamstat.teamid=team.teamid and team.teamid=game.awayid and game.gameid=%s',gameid)
  awayteam=[]
  for result in cursor:
    awayteam.append(result)
  cursor.close()
  cursor=g.conn.execute('SELECT a.playerid as playerid,a.pname as name,minute,fg,fga,fgp,tpt,tpta,tptp,ft,fta,ftg,orb,drb,trb,ast,stl,blk,tov,psf,pts,plusminus FROM playerstat,game,(select player.name as pname,playerof.teamid,player.playerid from player,playerof where player.playerid=playerof.playerid and playerof.year=2019) as a where a.playerid=playerstat.playerid and a.teamid=game.homeid and game.gameid=playerstat.gameid and game.gameid=%s',gameid)
  homepersonal=[]
  for result in cursor:
    homepersonal.append(result)
  cursor.close()
  cursor=g.conn.execute('SELECT a.playerid as playerid,a.pname as name,minute,fg,fga,fgp,tpt,tpta,tptp,ft,fta,ftg,orb,drb,trb,ast,stl,blk,tov,psf,pts,plusminus FROM playerstat,game,(select player.name as pname,playerof.teamid,player.playerid from player,playerof where player.playerid=playerof.playerid and playerof.year=2019) as a where a.playerid=playerstat.playerid and a.teamid=game.awayid and game.gameid=playerstat.gameid and game.gameid=%s',gameid)
  awaypersonal=[]
  for result in cursor:
    awaypersonal.append(result)
  cursor.close()
  return render_template('game.html',hometeam=hometeam,awayteam=awayteam,homepersonal=homepersonal,awaypersonal=awaypersonal)

# Example of adding new data to the database
#@app.route('/add', methods=['POST'])
#def add():
#  name = request.form['name']
#  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#  return redirect('/')


#@app.route('/login')
#def login():
#    abort(401)
#    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help
    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
