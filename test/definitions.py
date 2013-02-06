#coding: utf-8

from pyros.database import Table


test1 = Table(table = "test", primary = "id_test", fields = ['valor1#s', 'valor2#s'], joined = [{"table": "test2", "fields": ["id_test2 AS tablita"], "cond": "test.id_test = test2.id_test AND prueba = 42"}], suffix="_test")
test2 = Table(table = "test2", primary = "id_test2", fields = ["prueba"], readfields = ["timestamp"])
test3 = Table(table = "test3", primary = "id_test3")

test1.add_relation(test2, tag = "subtest")
test2.add_relation(test3, tag = "internal")
