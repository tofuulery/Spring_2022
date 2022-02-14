def replace_q_symbols(query_string):
  query_str = query_string
  query_symbls = ['|', '+', '%']
  pipe = str(query_symbls[0])
  plus_sign = str(query_symbls[1])
  pct_sign = str(query_symbls[2])
  or_str = ' OR '
  and_str = ' AND '
  pct_space_str = ' '
  if str(query_symbls[0]) in query_str:
      # q_str = re.sub(str(query_symbls[0]), repl=or_str, string=query_str, count=10)
      q_str = query_str.replace(pipe, or_str)
      if str(query_symbls[1]) in q_str:
          q_str2 = q_str.replace(plus_sign, and_str)
          if str(query_symbls[2]) in q_str2:
              q_str3 = q_str2.replace(pct_sign, pct_space_str)
              return q_str3
          else:
              return q_str2
      else:
          return q_str
