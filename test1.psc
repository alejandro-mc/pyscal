PROGRAM ASSIGNMENT;

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



{while b < 20 do
begin

b:= b + 1;
end;}


{sort the array}
{a:=1;
b:=1;
repeat 
  begin
      while b < 20 do
          begin
            if d[b] > d[b+1] then
               begin 
               c:= d[b];
               d[b] := d[b+1];
               d[b+1] := c;
               end;
            b:= b+1;
          end;
  b:=1;
  end;
until a > 20;} 


{fibonacci numbers}
{d[0] := 1;
d[1] := 1;
for i := 2 to 5 do
d[i] := d[i-1] + d[i-2];}



{array assignment}
{for i := 0 to 5 do
	begin
	d[i] := i * 2;
	e[i] := i * 2 + 1;
	end;}

{this is the best program ever written}
{a := 3 + 5 * 2 ;

b:= 1 + 2;

c:= a div 4;}
{if 3 > 2 then 
    c := 1;
else
	c := 0;}


{test while do}
{a:=0;

while a > 2 do 
      a:= a + 1;} 

{test do while}
{a:=1;

do a := a+1;
while a < 100 ;}

{factorial program}
{a:=10;
b:=1;
repeat
begin 
b:= b * a;
a:= a - 1;
end;
until a < 1 ;}

{for loop test}
{a := 0;
for z := 1 to 100 do
	a := a + 1;}

END.
