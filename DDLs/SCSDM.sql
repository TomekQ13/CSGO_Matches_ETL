--------------------------------------------------------
--  File created - niedziela-paüdziernika-18-2020   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table SCSDM_HEAD_TO_HEAD
--------------------------------------------------------

  CREATE TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" 
   (	"HEAD_TO_HEAD_RK" NUMBER(*,0), 
	"INSERT_DTTM" TIMESTAMP (6) DEFAULT current_timestamp, 
	"MATCH_RK" NUMBER(*,0), 
	"LT_NAME" VARCHAR2(255 CHAR), 
	"RT_NAME" VARCHAR2(255 CHAR), 
	"MAP_NAME" VARCHAR2(255 CHAR), 
	"LT_SCORE" NUMBER(*,0), 
	"RT_SCORE" NUMBER(*,0), 
	"TOURNAMENT" VARCHAR2(255 CHAR), 
	"REAL_MATCH_RK" NUMBER(*,0)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;

   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."HEAD_TO_HEAD_RK" IS 'Retained key for the table. Generated always as identity in the transformation layer.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."INSERT_DTTM" IS 'Row insert timestamp.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."MATCH_RK" IS 'Retained key for the match the  head to head belongs to. Generated in the transformation layer.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."LT_NAME" IS 'The name of the left team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."RT_NAME" IS 'The name of the right team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."MAP_NAME" IS 'The name of the map the match was played on.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."LT_SCORE" IS 'The score of the left team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."RT_SCORE" IS 'The score of the right team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."TOURNAMENT" IS 'The name of the tournament the match was played in.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"."REAL_MATCH_RK" IS 'The retained key for the same match in the MATCH table. May not be available.';
   COMMENT ON TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD"  IS 'Table contains informations abou head to head between the two teams for every match where head to head was available.';
--------------------------------------------------------
--  DDL for Table SCSDM_LINEUP
--------------------------------------------------------

  CREATE TABLE "C##TKUCZAK"."SCSDM_LINEUP" 
   (	"LINEUP_RK" NUMBER(*,0), 
	"INSERT_DTTM" TIMESTAMP (6) DEFAULT current_timestamp, 
	"MATCH_RK" NUMBER(*,0), 
	"LT_PLAYER_ONE" VARCHAR2(255 CHAR), 
	"LT_PLAYER_TWO" VARCHAR2(255 CHAR), 
	"LT_PLAYER_THREE" VARCHAR2(255 CHAR), 
	"LT_PLAYER_FOUR" VARCHAR2(255 CHAR), 
	"LT_PLAYER_FIVE" VARCHAR2(255 CHAR), 
	"RT_PLAYER_ONE" VARCHAR2(255 CHAR), 
	"RT_PLAYER_TWO" VARCHAR2(255 CHAR), 
	"RT_PLAYER_THREE" VARCHAR2(255 CHAR), 
	"RT_PLAYER_FOUR" VARCHAR2(255 CHAR), 
	"RT_PLAYER_FIVE" VARCHAR2(255 CHAR)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;

   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LINEUP_RK" IS 'The retained key for the lineup. Generated always as identity in the transformation layer.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."INSERT_DTTM" IS 'Insert timestamp of the row.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."MATCH_RK" IS 'Retained key for a match the lineup belogs to.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LT_PLAYER_ONE" IS 'Left team player one.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LT_PLAYER_TWO" IS 'Left team player two.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LT_PLAYER_THREE" IS 'Left team player three.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LT_PLAYER_FOUR" IS 'Left team player four.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."LT_PLAYER_FIVE" IS 'Left team player five.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."RT_PLAYER_ONE" IS 'Right team player one.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."RT_PLAYER_TWO" IS 'Right team player two.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."RT_PLAYER_THREE" IS 'Right team player three.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."RT_PLAYER_FOUR" IS 'Right team player four.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_LINEUP"."RT_PLAYER_FIVE" IS 'Right team player five.';
   COMMENT ON TABLE "C##TKUCZAK"."SCSDM_LINEUP"  IS 'The table containes information about lineups for each team for the match.';
--------------------------------------------------------
--  DDL for Table SCSDM_MAP
--------------------------------------------------------

  CREATE TABLE "C##TKUCZAK"."SCSDM_MAP" 
   (	"MAP_RK" NUMBER(*,0), 
	"INSERT_DTTM" TIMESTAMP (6), 
	"MATCH_RK" NUMBER(*,0), 
	"MAP_NAME" VARCHAR2(255 CHAR), 
	"MAP_NUMBER" NUMBER(*,0), 
	"LT_SCORE" NUMBER(*,0), 
	"RT_SCORE" NUMBER(*,0)
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;

   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MAP"."MATCH_RK" IS 'The retained key of the match.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MAP"."MAP_NAME" IS 'The name of the map the match was played on.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MAP"."MAP_NUMBER" IS 'The number of the map in the match.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MAP"."LT_SCORE" IS 'The score of the left team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MAP"."RT_SCORE" IS 'The score of the right team.';
   COMMENT ON TABLE "C##TKUCZAK"."SCSDM_MAP"  IS 'The table stores information about maps played in a match.';
--------------------------------------------------------
--  DDL for Table SCSDM_MATCH
--------------------------------------------------------

  CREATE TABLE "C##TKUCZAK"."SCSDM_MATCH" 
   (	"MATCH_RK" NUMBER(*,0), 
	"LT_NAME" VARCHAR2(255 CHAR), 
	"RT_NAME" VARCHAR2(255 CHAR), 
	"LT_NATIONALITY" VARCHAR2(255 CHAR), 
	"LT_RANKING" VARCHAR2(255 CHAR), 
	"RT_NATIONALITY" VARCHAR2(255 CHAR), 
	"RT_RANKING" VARCHAR2(255 CHAR), 
	"TORUNAMENT" VARCHAR2(255 CHAR), 
	"MATCH_HOUR" VARCHAR2(255 CHAR), 
	"MATCH_DAY" VARCHAR2(255 CHAR), 
	"MATCH_MONTH" VARCHAR2(255 CHAR), 
	"YEAR_OF_THE_MATCH" VARCHAR2(255 CHAR), 
	"INSERT_DTTM" TIMESTAMP (6) DEFAULT current_timestamp
   ) SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  TABLESPACE "USERS" ;

   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."MATCH_RK" IS 'The match retained key. Generated always as identity in the transformation layer.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."LT_NAME" IS 'The name of the left team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."RT_NAME" IS 'The name of the right team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."LT_NATIONALITY" IS 'The nationality of the left team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."LT_RANKING" IS 'The place in the HLTV ranking of the left team at the time the match was played.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."RT_NATIONALITY" IS 'The nationality of the right team.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."RT_RANKING" IS 'The place in the HLTV ranking of the right team at the time the match was played.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."TORUNAMENT" IS 'The torunament the match was played in.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."MATCH_HOUR" IS 'The hour the match was played at.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."MATCH_DAY" IS 'The day of the month the match was played.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."MATCH_MONTH" IS 'The month the match was played.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."YEAR_OF_THE_MATCH" IS 'The year the match was played in.';
   COMMENT ON COLUMN "C##TKUCZAK"."SCSDM_MATCH"."INSERT_DTTM" IS 'Insert timestamp of the row.';
   COMMENT ON TABLE "C##TKUCZAK"."SCSDM_MATCH"  IS 'The table contains information about matches.';
--------------------------------------------------------
--  DDL for Index SCSDM_HEAD_TO_HEAD_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD_PK" ON "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" ("HEAD_TO_HEAD_RK") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  DDL for Index SCSDM_LINEUP_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "C##TKUCZAK"."SCSDM_LINEUP_PK" ON "C##TKUCZAK"."SCSDM_LINEUP" ("LINEUP_RK") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  DDL for Index SCSDM_MAP_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "C##TKUCZAK"."SCSDM_MAP_PK" ON "C##TKUCZAK"."SCSDM_MAP" ("MAP_RK") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  DDL for Index SCSDM_MATCH_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "C##TKUCZAK"."SCSDM_MATCH_PK" ON "C##TKUCZAK"."SCSDM_MATCH" ("MATCH_RK") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  Constraints for Table SCSDM_HEAD_TO_HEAD
--------------------------------------------------------

  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("HEAD_TO_HEAD_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("INSERT_DTTM" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("MATCH_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("LT_NAME" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("RT_NAME" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("MAP_NAME" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("LT_SCORE" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("RT_SCORE" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" MODIFY ("TOURNAMENT" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_HEAD_TO_HEAD" ADD CONSTRAINT "SCSDM_HEAD_TO_HEAD_PK" PRIMARY KEY ("HEAD_TO_HEAD_RK")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
--------------------------------------------------------
--  Constraints for Table SCSDM_LINEUP
--------------------------------------------------------

  ALTER TABLE "C##TKUCZAK"."SCSDM_LINEUP" MODIFY ("LINEUP_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_LINEUP" MODIFY ("INSERT_DTTM" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_LINEUP" MODIFY ("MATCH_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_LINEUP" ADD CONSTRAINT "SCSDM_LINEUP_PK" PRIMARY KEY ("LINEUP_RK")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
--------------------------------------------------------
--  Constraints for Table SCSDM_MAP
--------------------------------------------------------

  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" MODIFY ("MAP_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" MODIFY ("MATCH_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" MODIFY ("MAP_NUMBER" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" MODIFY ("LT_SCORE" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" MODIFY ("RT_SCORE" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MAP" ADD CONSTRAINT "SCSDM_MAP_PK" PRIMARY KEY ("MAP_RK")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
--------------------------------------------------------
--  Constraints for Table SCSDM_MATCH
--------------------------------------------------------

  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("MATCH_RK" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("LT_NAME" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("RT_NAME" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("TORUNAMENT" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("MATCH_HOUR" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("MATCH_DAY" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("MATCH_MONTH" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("YEAR_OF_THE_MATCH" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" MODIFY ("INSERT_DTTM" NOT NULL ENABLE);
  ALTER TABLE "C##TKUCZAK"."SCSDM_MATCH" ADD CONSTRAINT "SCSDM_MATCH_PK" PRIMARY KEY ("MATCH_RK")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS 
  TABLESPACE "USERS"  ENABLE;
