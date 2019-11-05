edit:
	gcc studentsseq.c -o studentsseq.bin -lm
	mpicc studentspar_master.c -o studentspar_master.bin -lm
	mpicc studentspar_slave.c -o studentspar_slave.bin -lm

run:
	./studentsseq.bin 3 4 6 154
	mpirun --oversubscribe -np 1 studentspar_master.bin 3 4 6 154

clean:
	rm *.bin