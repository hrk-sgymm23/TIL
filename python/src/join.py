# list
list_data = ["f", "u", "g", "a"]
joined_list_data = "".join(list_data)
# fuga
print(joined_list_data)

# tuple
tuple_data = ("a","b","c","d")
joined_tuple_data = "".join(tuple_data)
# abcd
print(joined_tuple_data)

# str
str_data = ("hoge")
joined_str_data = "/".join(str_data)
# h/o/g/e
print(joined_str_data)

# dict
dict_data =  { "name": "hige", "age": 23, "address": "shinjuku" }
joined_dict_data = "/".join(dict_data)
# keyのみ結合される
# name/age/address
print(joined_dict_data)

# valueを結合したい場合
dict_data2 =  { "name": "higa", "age": 24, "address": "shibuya" }
joined_dict2_data = "/".join(str(value) for value in dict_data2.values())
# higa/24/shibuya
print(joined_dict2_data)
