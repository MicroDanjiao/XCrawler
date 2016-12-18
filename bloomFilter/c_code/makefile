objects = bloom_filter.o hash_func.o

bloom_filter : $(object)
	gcc -o bloom_filter $(objects)

bloom_filter.o : bloom_filter.h hash_func.c hash_func.h
	gcc -c bloom_filter.c

hash_func.o : hash_func.c hash_func.h
	gcc -c hash_func.c

clean :
	rm bloom_filter $(objects)
