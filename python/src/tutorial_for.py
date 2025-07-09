# コレクション作成
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# 方針:  コピーを反復
for user, status in users.copy().items():
    print(user, status)
    if status == 'inactive':
        print (users[user])

# 方針:  新コレクション作成
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

        print(active_users)