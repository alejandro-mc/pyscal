PROGRAM BUBLESORST;

var a,b,c : integer;

var d : array[1 .. 20] of integer;

BEGIN

{bubble sort}

{initialize array in decreasing order}
a:=21;
{i goes to memory location 23 
(note for simplicity integers take only one memory location in my stack machine)}
for i:= 1 to 20 do
	begin
	d[i] := a;
	a:= a - 1;
	end;

{sort array in increasing order}
a:=1;{goes to memory location 0}
b:=1;{goes to memory location 1}
     {d goes to memory locations 2 to 22}
while b <= 20 do
begin
    while a <= 20 - b do
	begin
	   if d[a] > d[a + 1] then
	   begin
	   c      := d[a];
	   d[a]   := d[a + 1];
	   d[a + 1] := c;
	   end;

	a:= a + 1;
 	end;

    b := b + 1;
    a := 1;
end;


END.
