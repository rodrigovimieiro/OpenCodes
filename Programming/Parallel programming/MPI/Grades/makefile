edit:
	gcc studentsseq.c -o studentsseq.bin -lm
	mpicc studentspar_master.c -o studentspar_master.bin -lm
	mpicc studentspar_slave.c -o studentspar_slave.bin -lm

run:
	./studentsseq.bin 3 4 6 154
	mpirun --use-hwthread-cpus -hostfile halley.txt -np 1 studentspar_master.bin 300 600 10 100

clean:
	rm *.bin
