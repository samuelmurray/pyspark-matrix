.PHONY: default clean

default:
	@ echo Run \"make clean\" to remove all downloaded files

clean:
	rm -fv *.mat
