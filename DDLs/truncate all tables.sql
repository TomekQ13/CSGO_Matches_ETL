truncate table C##TKUCZAK.TR_HEAD_TO_HEAD;
truncate table C##TKUCZAK.TR_LINEUP;
truncate table C##TKUCZAK.TR_MAP;
truncate table C##TKUCZAK.TR_MATCH;

truncate table C##TKUCZAK.SCSDM_HEAD_TO_HEAD;
truncate table C##TKUCZAK.SCSDM_LINEUP;
truncate table C##TKUCZAK.SCSDM_MAP;
truncate table C##TKUCZAK.SCSDM_MATCH;

truncate table C##TKUCZAK.EX_FINAL_DICTIONARY;
truncate table C##TKUCZAK.EX_HEAD_TO_HEAD;
truncate table C##TKUCZAK.EX_RESULTS_PDF;
truncate table C##TKUCZAK.EX_TEAMS_PAST_MATCHES;

truncate table C##TKUCZAK.TR_MAP_MATCH_RK;

truncate table C##TKUCZAK.LOAD_STATUS;


commit;

select * from C##TKUCZAK.TR_MAP where lt_score is null;

select * from C##TKUCZAK.EX_RESULTS_PDF where TEAM_LEFT_SCORE is null;


