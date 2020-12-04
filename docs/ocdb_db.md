```plantuml
digraph model_graph {
  // Dotfile by Django-Extensions graph_models
  // Created: 2020-12-03 22:09
  // Cli Options: ocdb --dot -o ./docs/ocdb_db.dot

  fontname = "Roboto"
  fontsize = 8
  splines  = true

  node [
    fontname = "Roboto"
    fontsize = 8
    shape = "plaintext"
  ]

  edge [
    fontname = "Roboto"
    fontsize = 8
  ]

  // Labels


  ocdb_models_GradeSystemType [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    GradeSystemType
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_GradeSystem [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    GradeSystem
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_grade_system_type</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Grade [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Grade
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_grade_system</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">weight</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">IntegerField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_RouteCharacter [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    RouteCharacter
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Light [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Light
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Orientation [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Orientation
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_RockType [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    RockType
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_AscentStyle [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    AscentStyle
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Diary [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Diary
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">date</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">DateField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">description</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Person [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Person
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">last_name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">nick_name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_DiaryPerson [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    DiaryPerson
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_diary</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_person</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Sector [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Sector
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_light</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_orientation</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_sector</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">altitude</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">FloatField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">ascent_description</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">ascent_time_min</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">IntegerField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">child_friendly</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">BooleanField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">descent_description</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">latitude</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">FloatField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">longitude</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">FloatField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">max_height_in_m</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">IntegerField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">rain_protected</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">BooleanField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">windy</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">BooleanField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_Route [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    Route
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">description</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">equipment</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">hints</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">length_in_m</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">IntegerField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto">name</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT COLOR="#7B7B7B" FACE="Roboto">protection</FONT>
    </TD><TD ALIGN="LEFT">
    <FONT COLOR="#7B7B7B" FACE="Roboto">CharField</FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_RouteRouteCharacter [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    RouteRouteCharacter
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_route</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_route_character</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
    </TABLE>
    >]

  ocdb_models_RouteGrades [label=<
    <TABLE BGCOLOR="white" BORDER="1" CELLBORDER="0" CELLSPACING="0">
    <TR><TD COLSPAN="2" CELLPADDING="5" ALIGN="CENTER" BGCOLOR="#1b563f">
    <FONT FACE="Roboto" COLOR="white" POINT-SIZE="10"><B>
    RouteGrades
    </B></FONT></TD></TR>
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>id</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>AutoField</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_ascent_style</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_grade</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
  
    <TR><TD ALIGN="LEFT" BORDER="0">
    <FONT FACE="Roboto"><B>fk_route</B></FONT>
    </TD><TD ALIGN="LEFT">
    <FONT FACE="Roboto"><B>ForeignKey (id)</B></FONT>
    </TD></TR>
  
  
    </TABLE>
    >]




  // Relations

  ocdb_models_GradeSystem -> ocdb_models_GradeSystemType
  [label=" fk_grade_system_type (grade_system_types)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_Grade -> ocdb_models_GradeSystem
  [label=" fk_grade_system (grade_systems)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_DiaryPerson -> ocdb_models_Person
  [label=" fk_person (persons)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_DiaryPerson -> ocdb_models_Diary
  [label=" fk_diary (diaries)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_Sector -> ocdb_models_Sector
  [label=" fk_sector (sectors)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_Sector -> ocdb_models_Orientation
  [label=" fk_orientation (orientations)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_Sector -> ocdb_models_Light
  [label=" fk_light (lights)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_RouteRouteCharacter -> ocdb_models_Route
  [label=" fk_route (routes)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_RouteRouteCharacter -> ocdb_models_RouteCharacter
  [label=" fk_route_character (route_characters)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_RouteGrades -> ocdb_models_Route
  [label=" fk_route (grade_routes)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_RouteGrades -> ocdb_models_AscentStyle
  [label=" fk_ascent_style (route_characters)"] [arrowhead=none, arrowtail=dot, dir=both];

  ocdb_models_RouteGrades -> ocdb_models_Grade
  [label=" fk_grade (routes)"] [arrowhead=none, arrowtail=dot, dir=both];


}
'''