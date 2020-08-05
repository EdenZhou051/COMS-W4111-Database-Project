# COMS-W4111-Database-Project

This is a course project. 

Overview of the Project
You will build a substantial real-world database application of your choice. This project is split into three parts:
Part 1: You will come up with an application of interest to you and you will design the associated database.
Part 2: You will implement your database design on PostgreSQL, including example data.
Part 3: You will write an application in Python that manipulates the database through updates and queries, through a simple web front-end.
Part 4: You will extend the schema of Part 1 with object-relational features.

Our database intends to focus on National Basketball Association (NBA) statistics for players and teams during 2018-2019 series.

We plan on creating approximately 7 entities and 7 relationships in our database. The entities are PLAYER, PLAYER STAT, TEAM, TEAM STAT, GAME, SERIE and COACH. 
Each entity has multiple attributes. For example,PLAYER has attributes: playerID (primary key), Name (not null), Date of Birth, Position, Shooting Hand, etc.

The general relationships are, for each season, there are plenty of games. Players of a team participate in games. Each player has personal stats and each team has team stats. 
Coaches are instructors of teams.

Right now we have approximately 10 tables in our database, advanced statistics can be made by calculation.
