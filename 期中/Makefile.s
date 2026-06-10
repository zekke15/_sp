CC=gcc
CFLAGS=-Wall -g

OBJS=main.o lexer.o parser.o eval.o symbol_table.o

interpreter: $(OBJS)
$(CC) $(CFLAGS) -o interpreter $(OBJS)

clean:
rm -f *.o interpret