#module will consist of function to manage sql


class db_con:
   #this class is supoosed to make executing queries and retrieving results very easy      
   
   
   def __init__(self, connect_string = 'oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521'):
                import sqlalchemy as sql
                
                
                self.engine = sql.create_engine(connect_string)
                self.connect_string = 'oracle+cx_oracle://C##tkuczak:TOMCIO@@@@localhost:1521'
                                                    
   def truncate_interface(self,
                          query1 = 'truncate table C##TKUCZAK.IF_HEAD_TO_HEAD',
                          query2 = 'truncate table C##TKUCZAK.IF_RESULTS_PDF',
                          query3 = 'truncate table C##TKUCZAK.IF_TEAMS_PAST_MATCHES',
                          query4 = 'delete from C##TKUCZAK.IF_FINAL_DICTIONARY'):
                          self.engine.execute(query1)
                          self.engine.execute(query2)
                          self.engine.execute(query3)
                          self.engine.execute(query4)
                          
                          
                          def select_to_pandas(sql, con = self.engine):
                             import pandas as pd
                             pd.read_sql(sql, con)

                          
                            
                          