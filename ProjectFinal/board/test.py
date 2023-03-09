import json
f= open('board.txt','r',encoding='utf-8')

board = []
for line in f.readlines():
    board.append(line.split(','))
print(board)

board = ['id', 'title', 'contents' , 'substance', 'write_dttm', 'board_name', 'update_dttm', 'hits','files', 'filename', 'accept','like_count','dislike_count', 'category','follow_count', 'writer_id']




