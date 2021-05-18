; This file is mostly generated from the C code, with just a touch of cleanup
; by hand to make it more portable and legible.

; Imports from the C library

%_IO_FILE = type opaque

@stdin = external global %_IO_FILE*
@stderr = external global %_IO_FILE*

declare void @exit(i32)
declare i32 @fprintf(%_IO_FILE*, i8*, ...)
declare void @free(i8*)
declare i32 @getc(%_IO_FILE*)
declare i32 @isspace(i32)
declare i8* @malloc(i64)
declare i32 @printf(i8*, ...)
declare i8* @realloc(i8*, i64)
declare i64 @strlen(i8*)
declare i32 @strncmp(i8*, i8*, i64)
declare i64 @strtoll(i8*, i8**, i32)
declare i32 @ungetc(i32, %_IO_FILE*)

; Types for Object instances and vtable

%Object = type { %ObjectVTable* }
%ObjectVTable = type { %Object* (%Object*, i8*)*, %Object* (%Object*, i1)*, %Object* (%Object*, i32)*, i8* (%Object*)*, i1 (%Object*)*, i32 (%Object*)* }

; String literals

@.str = constant [3 x i8] c"%s\00"
@.str.1 = constant [5 x i8] c"true\00"
@.str.2 = constant [6 x i8] c"false\00"
@.str.3 = constant [3 x i8] c"%d\00"
@.str.4 = constant [1 x i8] zeroinitializer
@.str.5 = constant [38 x i8] c"Object::inputBool: cannot read word!\0A\00"
@.str.6 = constant [49 x i8] c"Object::inputBool: `%s` is not a valid boolean!\0A\00"
@.str.7 = constant [39 x i8] c"Object::inputInt32: cannot read word!\0A\00"
@.str.8 = constant [58 x i8] c"Object::inputInt32: `%s` is not a valid integer literal!\0A\00"
@.str.9 = constant [57 x i8] c"Object::inputInt32: `%s` does not fit a 32-bit integer!\0A\00"

; Object's shared vtable instance

@Object___vtable = constant %ObjectVTable { %Object* (%Object*, i8*)* @Object__print, %Object* (%Object*, i1)* @Object__printBool, %Object* (%Object*, i32)* @Object__printInt32, i8* (%Object*)* @Object__inputLine, i1 (%Object*)* @Object__inputBool, i32 (%Object*)* @Object__inputInt32 }

; Object's methods

define %Object* @Object__print(%Object*, i8*) {
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i8* %1)
  ret %Object* %0
}

define %Object* @Object__printBool(%Object*, i1 zeroext) {
  %3 = zext i1 %1 to i8
  %4 = trunc i8 %3 to i1
  %5 = zext i1 %4 to i64
  %6 = select i1 %4, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.2, i64 0, i64 0)
  %7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i8* %6)
  ret %Object* %0
}

define %Object* @Object__printInt32(%Object*, i32) {
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.3, i64 0, i64 0), i32 %1)
  ret %Object* %0
}

define i8* @Object__inputLine(%Object*) {
  %2 = call i8* @read_until(i32 (i32)* @is_eol)
  %3 = icmp ne i8* %2, null
  br i1 %3, label %5, label %4

4:                                                ; preds = %1
  br label %5

5:                                                ; preds = %4, %1
  %.0 = phi i8* [ %2, %1 ], [ getelementptr inbounds ([1 x i8], [1 x i8]* @.str.4, i64 0, i64 0), %4 ]
  ret i8* %.0
}

define zeroext i1 @Object__inputBool(%Object*) {
  call void @skip_while(i32 (i32)* @isspace)
  %2 = call i8* @read_until(i32 (i32)* @isspace)
  %3 = icmp ne i8* %2, null
  br i1 %3, label %7, label %4

4:                                                ; preds = %1
  %5 = load %_IO_FILE*, %_IO_FILE** @stderr
  %6 = call i32 (%_IO_FILE*, i8*, ...) @fprintf(%_IO_FILE* %5, i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.5, i64 0, i64 0))
  call void @exit(i32 1)
  unreachable

7:                                                ; preds = %1
  %8 = call i64 @strlen(i8* %2)
  %9 = icmp eq i64 %8, 4
  br i1 %9, label %10, label %14

10:                                               ; preds = %7
  %11 = call i32 @strncmp(i8* %2, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i64 4)
  %12 = icmp eq i32 %11, 0
  br i1 %12, label %13, label %14

13:                                               ; preds = %10
  call void @free(i8* %2)
  br label %23

14:                                               ; preds = %10, %7
  %15 = icmp eq i64 %8, 5
  br i1 %15, label %16, label %20

16:                                               ; preds = %14
  %17 = call i32 @strncmp(i8* %2, i8* getelementptr inbounds ([6 x i8], [6 x i8]* @.str.2, i64 0, i64 0), i64 5)
  %18 = icmp eq i32 %17, 0
  br i1 %18, label %19, label %20

19:                                               ; preds = %16
  call void @free(i8* %2)
  br label %23

20:                                               ; preds = %16, %14
  %21 = load %_IO_FILE*, %_IO_FILE** @stderr
  %22 = call i32 (%_IO_FILE*, i8*, ...) @fprintf(%_IO_FILE* %21, i8* getelementptr inbounds ([49 x i8], [49 x i8]* @.str.6, i64 0, i64 0), i8* %2)
  call void @free(i8* %2)
  call void @exit(i32 1)
  unreachable

23:                                               ; preds = %19, %13
  %.0 = phi i1 [ true, %13 ], [ false, %19 ]
  ret i1 %.0
}

define i32 @Object__inputInt32(%Object*) {
  %2 = alloca i8*
  call void @skip_while(i32 (i32)* @isspace)
  %3 = call i8* @read_until(i32 (i32)* @isspace)
  %4 = icmp ne i8* %3, null
  br i1 %4, label %8, label %5

5:                                                ; preds = %1
  %6 = load %_IO_FILE*, %_IO_FILE** @stderr
  %7 = call i32 (%_IO_FILE*, i8*, ...) @fprintf(%_IO_FILE* %6, i8* getelementptr inbounds ([39 x i8], [39 x i8]* @.str.7, i64 0, i64 0))
  call void @exit(i32 1)
  unreachable

8:                                                ; preds = %1
  %9 = call i64 @strlen(i8* %3)
  %10 = icmp ugt i64 %9, 2
  br i1 %10, label %11, label %21

11:                                               ; preds = %8
  %12 = getelementptr inbounds i8, i8* %3, i64 0
  %13 = load i8, i8* %12
  %14 = sext i8 %13 to i32
  %15 = icmp eq i32 %14, 48
  br i1 %15, label %16, label %21

16:                                               ; preds = %11
  %17 = getelementptr inbounds i8, i8* %3, i64 1
  %18 = load i8, i8* %17
  %19 = sext i8 %18 to i32
  %20 = icmp eq i32 %19, 120
  br i1 %20, label %45, label %21

21:                                               ; preds = %16, %11, %8
  %22 = icmp ugt i64 %9, 3
  br i1 %22, label %23, label %43

23:                                               ; preds = %21
  %24 = getelementptr inbounds i8, i8* %3, i64 0
  %25 = load i8, i8* %24
  %26 = sext i8 %25 to i32
  %27 = icmp eq i32 %26, 43
  br i1 %27, label %33, label %28

28:                                               ; preds = %23
  %29 = getelementptr inbounds i8, i8* %3, i64 0
  %30 = load i8, i8* %29
  %31 = sext i8 %30 to i32
  %32 = icmp eq i32 %31, 45
  br i1 %32, label %33, label %43

33:                                               ; preds = %28, %23
  %34 = getelementptr inbounds i8, i8* %3, i64 1
  %35 = load i8, i8* %34
  %36 = sext i8 %35 to i32
  %37 = icmp eq i32 %36, 48
  br i1 %37, label %38, label %43

38:                                               ; preds = %33
  %39 = getelementptr inbounds i8, i8* %3, i64 2
  %40 = load i8, i8* %39
  %41 = sext i8 %40 to i32
  %42 = icmp eq i32 %41, 120
  br label %43

43:                                               ; preds = %38, %33, %28, %21
  %44 = phi i1 [ false, %33 ], [ false, %28 ], [ false, %21 ], [ %42, %38 ]
  br label %45

45:                                               ; preds = %43, %16
  %46 = phi i1 [ true, %16 ], [ %44, %43 ]
  %47 = zext i1 %46 to i8
  %48 = trunc i8 %47 to i1
  br i1 %48, label %49, label %51

49:                                               ; preds = %45
  %50 = call i64 @strtoll(i8* %3, i8** %2, i32 16)
  br label %53

51:                                               ; preds = %45
  %52 = call i64 @strtoll(i8* %3, i8** %2, i32 10)
  br label %53

53:                                               ; preds = %51, %49
  %.0 = phi i64 [ %50, %49 ], [ %52, %51 ]
  %54 = load i8*, i8** %2
  %55 = load i8, i8* %54
  %56 = sext i8 %55 to i32
  %57 = icmp ne i32 %56, 0
  br i1 %57, label %58, label %61

58:                                               ; preds = %53
  %59 = load %_IO_FILE*, %_IO_FILE** @stderr
  %60 = call i32 (%_IO_FILE*, i8*, ...) @fprintf(%_IO_FILE* %59, i8* getelementptr inbounds ([58 x i8], [58 x i8]* @.str.8, i64 0, i64 0), i8* %3)
  call void @exit(i32 1)
  unreachable

61:                                               ; preds = %53
  %62 = icmp slt i64 %.0, -2147483648
  br i1 %62, label %65, label %63

63:                                               ; preds = %61
  %64 = icmp sgt i64 %.0, 2147483647
  br i1 %64, label %65, label %68

65:                                               ; preds = %63, %61
  %66 = load %_IO_FILE*, %_IO_FILE** @stderr
  %67 = call i32 (%_IO_FILE*, i8*, ...) @fprintf(%_IO_FILE* %66, i8* getelementptr inbounds ([57 x i8], [57 x i8]* @.str.9, i64 0, i64 0), i8* %3)
  call void @exit(i32 1)
  unreachable

68:                                               ; preds = %63
  %69 = trunc i64 %.0 to i32
  ret i32 %69
}

; Object constructor and initializer

define %Object* @Object___new() {
  %1 = call i8* @malloc(i64 8)
  %2 = bitcast i8* %1 to %Object*
  %3 = call %Object* @Object___init(%Object* %2)
  ret %Object* %3
}

define %Object* @Object___init(%Object*) {
  %2 = icmp ne %Object* %0, null
  br i1 %2, label %3, label %5

3:                                                ; preds = %1
  %4 = getelementptr inbounds %Object, %Object* %0, i32 0, i32 0
  store %ObjectVTable* @Object___vtable, %ObjectVTable** %4
  br label %5

5:                                                ; preds = %3, %1
  ret %Object* %0
}

; Utility functions

define internal i8* @read_until(i32 (i32)*) {
  %2 = call i8* @malloc(i64 1024)
  br label %3

3:                                                ; preds = %29, %1
  %.03 = phi i8* [ %2, %1 ], [ %.14, %29 ]
  %.02 = phi i64 [ 1024, %1 ], [ %.1, %29 ]
  %.01 = phi i64 [ 0, %1 ], [ %30, %29 ]
  %4 = icmp ne i8* %.03, null
  br i1 %4, label %5, label %31

5:                                                ; preds = %3
  %6 = load %_IO_FILE*, %_IO_FILE** @stdin
  %7 = call i32 @getc(%_IO_FILE* %6)
  %8 = icmp eq i32 %7, -1
  br i1 %8, label %14, label %9

9:                                                ; preds = %5
  %10 = trunc i32 %7 to i8
  %11 = sext i8 %10 to i32
  %12 = call i32 %0(i32 %11)
  %13 = icmp ne i32 %12, 0
  br i1 %13, label %14, label %21

14:                                               ; preds = %9, %5
  %15 = icmp ne i32 %7, -1
  br i1 %15, label %16, label %19

16:                                               ; preds = %14
  %17 = load %_IO_FILE*, %_IO_FILE** @stdin
  %18 = call i32 @ungetc(i32 %7, %_IO_FILE* %17)
  br label %19

19:                                               ; preds = %16, %14
  %20 = getelementptr inbounds i8, i8* %.03, i64 %.01
  store i8 0, i8* %20
  br label %32

21:                                               ; preds = %9
  %22 = trunc i32 %7 to i8
  %23 = getelementptr inbounds i8, i8* %.03, i64 %.01
  store i8 %22, i8* %23
  %24 = sub i64 %.02, 1
  %25 = icmp eq i64 %.01, %24
  br i1 %25, label %26, label %29

26:                                               ; preds = %21
  %27 = mul i64 %.02, 2
  %28 = call i8* @realloc(i8* %.03, i64 %27)
  br label %29

29:                                               ; preds = %26, %21
  %.14 = phi i8* [ %28, %26 ], [ %.03, %21 ]
  %.1 = phi i64 [ %27, %26 ], [ %.02, %21 ]
  %30 = add i64 %.01, 1
  br label %3

31:                                               ; preds = %3
  br label %32

32:                                               ; preds = %31, %19
  %.0 = phi i8* [ %.03, %19 ], [ null, %31 ]
  ret i8* %.0
}

define internal i32 @is_eol(i32) {
  %2 = icmp eq i32 %0, 10
  %3 = zext i1 %2 to i32
  ret i32 %3
}

define internal void @skip_while(i32 (i32)*) {
  %2 = load %_IO_FILE*, %_IO_FILE** @stdin
  %3 = call i32 @getc(%_IO_FILE* %2)
  br label %4

4:                                                ; preds = %11, %1
  %.0 = phi i32 [ %3, %1 ], [ %13, %11 ]
  %5 = icmp ne i32 %.0, -1
  br i1 %5, label %6, label %9

6:                                                ; preds = %4
  %7 = call i32 %0(i32 %.0)
  %8 = icmp ne i32 %7, 0
  br label %9

9:                                                ; preds = %6, %4
  %10 = phi i1 [ false, %4 ], [ %8, %6 ]
  br i1 %10, label %11, label %14

11:                                               ; preds = %9
  %12 = load %_IO_FILE*, %_IO_FILE** @stdin
  %13 = call i32 @getc(%_IO_FILE* %12)
  br label %4

14:                                               ; preds = %9
  %15 = icmp ne i32 %.0, -1
  br i1 %15, label %16, label %19

16:                                               ; preds = %14
  %17 = load %_IO_FILE*, %_IO_FILE** @stdin
  %18 = call i32 @ungetc(i32 %.0, %_IO_FILE* %17)
  br label %19

19:                                               ; preds = %16, %14
  ret void
}



%"Main" = type {%"MainVT"*, i32}
%"MainVT" = type {%"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i1)*, %"Object"* (%"Object"*, i32)*, i8* (%"Object"*)*, i1 (%"Object"*)*, i32 (%"Object"*)*, i1 (%"Main"*)*, i32 (%"Main"*)*}
define i1 @"Main__guessN"(%"Main"* %".1") 
{
.3:
  %".4" = alloca %"Main"*
  store %"Main"* %".1", %"Main"** %".4"
  %".6" = load %"Main"*, %"Main"** %".4"
  %".7" = getelementptr inbounds %"Main", %"Main"* %".6", i32 0, i32 0
  %".8" = load %"MainVT"*, %"MainVT"** %".7"
  %".9" = getelementptr inbounds %"MainVT", %"MainVT"* %".8", i32 0, i32 0
  %".10" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".9"
  %".11" = getelementptr inbounds [5 x i8], [5 x i8]* @"string", i32 0, i32 0
  %".12" = bitcast %"Main"* %".6" to %"Object"*
  %".13" = call %"Object"* %".10"(%"Object"* %".12", i8* %".11")
  %".14" = getelementptr inbounds %"Object", %"Object"* %".13", i32 0, i32 0
  %".15" = load %"ObjectVTable"*, %"ObjectVTable"** %".14"
  %".16" = getelementptr inbounds %"ObjectVTable", %"ObjectVTable"* %".15", i32 0, i32 2
  %".17" = load %"Object"* (%"Object"*, i32)*, %"Object"* (%"Object"*, i32)** %".16"
  %".18" = load %"Main"*, %"Main"** %".4"
  %".19" = getelementptr inbounds %"Main", %"Main"* %".18", i32 0, i32 1
  %".20" = load i32, i32* %".19"
  %".21" = call %"Object"* %".17"(%"Object"* %".13", i32 %".20")
  %".22" = getelementptr inbounds %"Object", %"Object"* %".21", i32 0, i32 0
  %".23" = load %"ObjectVTable"*, %"ObjectVTable"** %".22"
  %".24" = getelementptr inbounds %"ObjectVTable", %"ObjectVTable"* %".23", i32 0, i32 0
  %".25" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".24"
  %".26" = getelementptr inbounds [12 x i8], [12 x i8]* @"string.1", i32 0, i32 0
  %".27" = call %"Object"* %".25"(%"Object"* %".21", i8* %".26")
  %".28" = alloca %"Object"*
  %".29" = load %"Main"*, %"Main"** %".4"
  %".30" = getelementptr inbounds %"Main", %"Main"* %".29", i32 0, i32 1
  %".31" = load i32, i32* %".30"
  %".32" = icmp ult i32 %".31", 0
  br i1 %".32", label %".3.if", label %".3.else"
.3.if:
  %".34" = load %"Main"*, %"Main"** %".4"
  %".35" = getelementptr inbounds %"Main", %"Main"* %".34", i32 0, i32 0
  %".36" = load %"MainVT"*, %"MainVT"** %".35"
  %".37" = getelementptr inbounds %"MainVT", %"MainVT"* %".36", i32 0, i32 0
  %".38" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".37"
  %".39" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.2", i32 0, i32 0
  %".40" = bitcast %"Main"* %".34" to %"Object"*
  %".41" = call %"Object"* %".38"(%"Object"* %".40", i8* %".39")
  store %"Object"* %".41", %"Object"** %".28"
  br label %".3.endif"
.3.else:
  %".44" = alloca %"Object"*
  %".45" = load %"Main"*, %"Main"** %".4"
  %".46" = getelementptr inbounds %"Main", %"Main"* %".45", i32 0, i32 1
  %".47" = load i32, i32* %".46"
  %".48" = icmp ult i32 100, %".47"
  br i1 %".48", label %".3.else.if", label %".3.else.else"
.3.endif:
  %".339" = load %"Object"*, %"Object"** %".28"
  %".340" = load %"Main"*, %"Main"** %".4"
  %".341" = getelementptr inbounds %"Main", %"Main"* %".340", i32 0, i32 0
  %".342" = load %"MainVT"*, %"MainVT"** %".341"
  %".343" = getelementptr inbounds %"MainVT", %"MainVT"* %".342", i32 0, i32 0
  %".344" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".343"
  %".345" = getelementptr inbounds [2 x i8], [2 x i8]* @"string.19", i32 0, i32 0
  %".346" = bitcast %"Main"* %".340" to %"Object"*
  %".347" = call %"Object"* %".344"(%"Object"* %".346", i8* %".345")
  ret i1 0
.3.else.if:
  %".50" = load %"Main"*, %"Main"** %".4"
  %".51" = getelementptr inbounds %"Main", %"Main"* %".50", i32 0, i32 0
  %".52" = load %"MainVT"*, %"MainVT"** %".51"
  %".53" = getelementptr inbounds %"MainVT", %"MainVT"* %".52", i32 0, i32 0
  %".54" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".53"
  %".55" = getelementptr inbounds [8 x i8], [8 x i8]* @"string.3", i32 0, i32 0
  %".56" = bitcast %"Main"* %".50" to %"Object"*
  %".57" = call %"Object"* %".54"(%"Object"* %".56", i8* %".55")
  store %"Object"* %".57", %"Object"** %".44"
  br label %".3.else.endif"
.3.else.else:
  %".60" = alloca %"Object"*
  %".61" = load %"Main"*, %"Main"** %".4"
  %".62" = getelementptr inbounds %"Main", %"Main"* %".61", i32 0, i32 1
  %".63" = load i32, i32* %".62"
  %".64" = icmp ult i32 %".63", 50
  br i1 %".64", label %".3.else.else.if", label %".3.else.else.else"
.3.else.endif:
  %".336" = load %"Object"*, %"Object"** %".44"
  store %"Object"* %".336", %"Object"** %".28"
  br label %".3.endif"
.3.else.else.if:
  %".66" = alloca %"Object"*
  %".67" = load %"Main"*, %"Main"** %".4"
  %".68" = getelementptr inbounds %"Main", %"Main"* %".67", i32 0, i32 1
  %".69" = load i32, i32* %".68"
  %".70" = icmp ult i32 %".69", 25
  br i1 %".70", label %".3.else.else.if.if", label %".3.else.else.if.else"
.3.else.else.else:
  %".323" = load %"Main"*, %"Main"** %".4"
  %".324" = getelementptr inbounds %"Main", %"Main"* %".323", i32 0, i32 0
  %".325" = load %"MainVT"*, %"MainVT"** %".324"
  %".326" = getelementptr inbounds %"MainVT", %"MainVT"* %".325", i32 0, i32 0
  %".327" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".326"
  %".328" = getelementptr inbounds [15 x i8], [15 x i8]* @"string.18", i32 0, i32 0
  %".329" = bitcast %"Main"* %".323" to %"Object"*
  %".330" = call %"Object"* %".327"(%"Object"* %".329", i8* %".328")
  store %"Object"* %".330", %"Object"** %".60"
  br label %".3.else.else.endif"
.3.else.else.endif:
  %".333" = load %"Object"*, %"Object"** %".60"
  store %"Object"* %".333", %"Object"** %".44"
  br label %".3.else.endif"
.3.else.else.if.if:
  %".72" = alloca %"Object"*
  %".73" = load %"Main"*, %"Main"** %".4"
  %".74" = getelementptr inbounds %"Main", %"Main"* %".73", i32 0, i32 1
  %".75" = load i32, i32* %".74"
  %".76" = icmp ult i32 %".75", 12
  br i1 %".76", label %".3.else.else.if.if.if", label %".3.else.else.if.if.else"
.3.else.else.if.else:
  %".310" = load %"Main"*, %"Main"** %".4"
  %".311" = getelementptr inbounds %"Main", %"Main"* %".310", i32 0, i32 0
  %".312" = load %"MainVT"*, %"MainVT"** %".311"
  %".313" = getelementptr inbounds %"MainVT", %"MainVT"* %".312", i32 0, i32 0
  %".314" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".313"
  %".315" = getelementptr inbounds [13 x i8], [13 x i8]* @"string.17", i32 0, i32 0
  %".316" = bitcast %"Main"* %".310" to %"Object"*
  %".317" = call %"Object"* %".314"(%"Object"* %".316", i8* %".315")
  store %"Object"* %".317", %"Object"** %".66"
  br label %".3.else.else.if.endif"
.3.else.else.if.endif:
  %".320" = load %"Object"*, %"Object"** %".66"
  store %"Object"* %".320", %"Object"** %".60"
  br label %".3.else.else.endif"
.3.else.else.if.if.if:
  %".78" = alloca %"Object"*
  %".79" = load %"Main"*, %"Main"** %".4"
  %".80" = getelementptr inbounds %"Main", %"Main"* %".79", i32 0, i32 1
  %".81" = load i32, i32* %".80"
  %".82" = icmp ult i32 %".81", 6
  br i1 %".82", label %".3.else.else.if.if.if.if", label %".3.else.else.if.if.if.else"
.3.else.else.if.if.else:
  %".297" = load %"Main"*, %"Main"** %".4"
  %".298" = getelementptr inbounds %"Main", %"Main"* %".297", i32 0, i32 0
  %".299" = load %"MainVT"*, %"MainVT"** %".298"
  %".300" = getelementptr inbounds %"MainVT", %"MainVT"* %".299", i32 0, i32 0
  %".301" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".300"
  %".302" = getelementptr inbounds [13 x i8], [13 x i8]* @"string.16", i32 0, i32 0
  %".303" = bitcast %"Main"* %".297" to %"Object"*
  %".304" = call %"Object"* %".301"(%"Object"* %".303", i8* %".302")
  store %"Object"* %".304", %"Object"** %".72"
  br label %".3.else.else.if.if.endif"
.3.else.else.if.if.endif:
  %".307" = load %"Object"*, %"Object"** %".72"
  store %"Object"* %".307", %"Object"** %".66"
  br label %".3.else.else.if.endif"
.3.else.else.if.if.if.if:
  %".84" = alloca %"Object"*
  %".85" = load %"Main"*, %"Main"** %".4"
  %".86" = getelementptr inbounds %"Main", %"Main"* %".85", i32 0, i32 1
  %".87" = load i32, i32* %".86"
  %".88" = icmp ult i32 %".87", 3
  br i1 %".88", label %".3.else.else.if.if.if.if.if", label %".3.else.else.if.if.if.if.else"
.3.else.else.if.if.if.else:
  %".189" = alloca %"Object"*
  %".190" = load %"Main"*, %"Main"** %".4"
  %".191" = getelementptr inbounds %"Main", %"Main"* %".190", i32 0, i32 1
  %".192" = load i32, i32* %".191"
  %".193" = icmp ult i32 %".192", 9
  br i1 %".193", label %".3.else.else.if.if.if.else.if", label %".3.else.else.if.if.if.else.else"
.3.else.else.if.if.if.endif:
  %".294" = load %"Object"*, %"Object"** %".78"
  store %"Object"* %".294", %"Object"** %".72"
  br label %".3.else.else.if.if.endif"
.3.else.else.if.if.if.if.if:
  %".90" = alloca %"Object"*
  %".91" = load %"Main"*, %"Main"** %".4"
  %".92" = getelementptr inbounds %"Main", %"Main"* %".91", i32 0, i32 1
  %".93" = load i32, i32* %".92"
  %".94" = icmp ult i32 %".93", 2
  br i1 %".94", label %".3.else.else.if.if.if.if.if.if", label %".3.else.else.if.if.if.if.if.else"
.3.else.else.if.if.if.if.else:
  %".138" = alloca %"Object"*
  %".139" = load %"Main"*, %"Main"** %".4"
  %".140" = getelementptr inbounds %"Main", %"Main"* %".139", i32 0, i32 1
  %".141" = load i32, i32* %".140"
  %".142" = icmp ult i32 %".141", 4
  br i1 %".142", label %".3.else.else.if.if.if.if.else.if", label %".3.else.else.if.if.if.if.else.else"
.3.else.else.if.if.if.if.endif:
  %".186" = load %"Object"*, %"Object"** %".84"
  store %"Object"* %".186", %"Object"** %".78"
  br label %".3.else.else.if.if.if.endif"
.3.else.else.if.if.if.if.if.if:
  %".96" = alloca %"Object"*
  %".97" = load %"Main"*, %"Main"** %".4"
  %".98" = getelementptr inbounds %"Main", %"Main"* %".97", i32 0, i32 1
  %".99" = load i32, i32* %".98"
  %".100" = icmp ult i32 %".99", 1
  br i1 %".100", label %".3.else.else.if.if.if.if.if.if.if", label %".3.else.else.if.if.if.if.if.if.else"
.3.else.else.if.if.if.if.if.else:
  %".125" = load %"Main"*, %"Main"** %".4"
  %".126" = getelementptr inbounds %"Main", %"Main"* %".125", i32 0, i32 0
  %".127" = load %"MainVT"*, %"MainVT"** %".126"
  %".128" = getelementptr inbounds %"MainVT", %"MainVT"* %".127", i32 0, i32 0
  %".129" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".128"
  %".130" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.6", i32 0, i32 0
  %".131" = bitcast %"Main"* %".125" to %"Object"*
  %".132" = call %"Object"* %".129"(%"Object"* %".131", i8* %".130")
  store %"Object"* %".132", %"Object"** %".90"
  br label %".3.else.else.if.if.if.if.if.endif"
.3.else.else.if.if.if.if.if.endif:
  %".135" = load %"Object"*, %"Object"** %".90"
  store %"Object"* %".135", %"Object"** %".84"
  br label %".3.else.else.if.if.if.if.endif"
.3.else.else.if.if.if.if.if.if.if:
  %".102" = load %"Main"*, %"Main"** %".4"
  %".103" = getelementptr inbounds %"Main", %"Main"* %".102", i32 0, i32 0
  %".104" = load %"MainVT"*, %"MainVT"** %".103"
  %".105" = getelementptr inbounds %"MainVT", %"MainVT"* %".104", i32 0, i32 0
  %".106" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".105"
  %".107" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.4", i32 0, i32 0
  %".108" = bitcast %"Main"* %".102" to %"Object"*
  %".109" = call %"Object"* %".106"(%"Object"* %".108", i8* %".107")
  store %"Object"* %".109", %"Object"** %".96"
  br label %".3.else.else.if.if.if.if.if.if.endif"
.3.else.else.if.if.if.if.if.if.else:
  %".112" = load %"Main"*, %"Main"** %".4"
  %".113" = getelementptr inbounds %"Main", %"Main"* %".112", i32 0, i32 0
  %".114" = load %"MainVT"*, %"MainVT"** %".113"
  %".115" = getelementptr inbounds %"MainVT", %"MainVT"* %".114", i32 0, i32 0
  %".116" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".115"
  %".117" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.5", i32 0, i32 0
  %".118" = bitcast %"Main"* %".112" to %"Object"*
  %".119" = call %"Object"* %".116"(%"Object"* %".118", i8* %".117")
  store %"Object"* %".119", %"Object"** %".96"
  br label %".3.else.else.if.if.if.if.if.if.endif"
.3.else.else.if.if.if.if.if.if.endif:
  %".122" = load %"Object"*, %"Object"** %".96"
  store %"Object"* %".122", %"Object"** %".90"
  br label %".3.else.else.if.if.if.if.if.endif"
.3.else.else.if.if.if.if.else.if:
  %".144" = load %"Main"*, %"Main"** %".4"
  %".145" = getelementptr inbounds %"Main", %"Main"* %".144", i32 0, i32 0
  %".146" = load %"MainVT"*, %"MainVT"** %".145"
  %".147" = getelementptr inbounds %"MainVT", %"MainVT"* %".146", i32 0, i32 0
  %".148" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".147"
  %".149" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.7", i32 0, i32 0
  %".150" = bitcast %"Main"* %".144" to %"Object"*
  %".151" = call %"Object"* %".148"(%"Object"* %".150", i8* %".149")
  store %"Object"* %".151", %"Object"** %".138"
  br label %".3.else.else.if.if.if.if.else.endif"
.3.else.else.if.if.if.if.else.else:
  %".154" = alloca %"Object"*
  %".155" = load %"Main"*, %"Main"** %".4"
  %".156" = getelementptr inbounds %"Main", %"Main"* %".155", i32 0, i32 1
  %".157" = load i32, i32* %".156"
  %".158" = icmp ult i32 %".157", 5
  br i1 %".158", label %".3.else.else.if.if.if.if.else.else.if", label %".3.else.else.if.if.if.if.else.else.else"
.3.else.else.if.if.if.if.else.endif:
  %".183" = load %"Object"*, %"Object"** %".138"
  store %"Object"* %".183", %"Object"** %".84"
  br label %".3.else.else.if.if.if.if.endif"
.3.else.else.if.if.if.if.else.else.if:
  %".160" = load %"Main"*, %"Main"** %".4"
  %".161" = getelementptr inbounds %"Main", %"Main"* %".160", i32 0, i32 0
  %".162" = load %"MainVT"*, %"MainVT"** %".161"
  %".163" = getelementptr inbounds %"MainVT", %"MainVT"* %".162", i32 0, i32 0
  %".164" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".163"
  %".165" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.8", i32 0, i32 0
  %".166" = bitcast %"Main"* %".160" to %"Object"*
  %".167" = call %"Object"* %".164"(%"Object"* %".166", i8* %".165")
  store %"Object"* %".167", %"Object"** %".154"
  br label %".3.else.else.if.if.if.if.else.else.endif"
.3.else.else.if.if.if.if.else.else.else:
  %".170" = load %"Main"*, %"Main"** %".4"
  %".171" = getelementptr inbounds %"Main", %"Main"* %".170", i32 0, i32 0
  %".172" = load %"MainVT"*, %"MainVT"** %".171"
  %".173" = getelementptr inbounds %"MainVT", %"MainVT"* %".172", i32 0, i32 0
  %".174" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".173"
  %".175" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.9", i32 0, i32 0
  %".176" = bitcast %"Main"* %".170" to %"Object"*
  %".177" = call %"Object"* %".174"(%"Object"* %".176", i8* %".175")
  store %"Object"* %".177", %"Object"** %".154"
  br label %".3.else.else.if.if.if.if.else.else.endif"
.3.else.else.if.if.if.if.else.else.endif:
  %".180" = load %"Object"*, %"Object"** %".154"
  store %"Object"* %".180", %"Object"** %".138"
  br label %".3.else.else.if.if.if.if.else.endif"
.3.else.else.if.if.if.else.if:
  %".195" = alloca %"Object"*
  %".196" = load %"Main"*, %"Main"** %".4"
  %".197" = getelementptr inbounds %"Main", %"Main"* %".196", i32 0, i32 1
  %".198" = load i32, i32* %".197"
  %".199" = icmp ult i32 %".198", 7
  br i1 %".199", label %".3.else.else.if.if.if.else.if.if", label %".3.else.else.if.if.if.else.if.else"
.3.else.else.if.if.if.else.else:
  %".243" = alloca %"Object"*
  %".244" = load %"Main"*, %"Main"** %".4"
  %".245" = getelementptr inbounds %"Main", %"Main"* %".244", i32 0, i32 1
  %".246" = load i32, i32* %".245"
  %".247" = icmp ult i32 %".246", 10
  br i1 %".247", label %".3.else.else.if.if.if.else.else.if", label %".3.else.else.if.if.if.else.else.else"
.3.else.else.if.if.if.else.endif:
  %".291" = load %"Object"*, %"Object"** %".189"
  store %"Object"* %".291", %"Object"** %".78"
  br label %".3.else.else.if.if.if.endif"
.3.else.else.if.if.if.else.if.if:
  %".201" = load %"Main"*, %"Main"** %".4"
  %".202" = getelementptr inbounds %"Main", %"Main"* %".201", i32 0, i32 0
  %".203" = load %"MainVT"*, %"MainVT"** %".202"
  %".204" = getelementptr inbounds %"MainVT", %"MainVT"* %".203", i32 0, i32 0
  %".205" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".204"
  %".206" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.10", i32 0, i32 0
  %".207" = bitcast %"Main"* %".201" to %"Object"*
  %".208" = call %"Object"* %".205"(%"Object"* %".207", i8* %".206")
  store %"Object"* %".208", %"Object"** %".195"
  br label %".3.else.else.if.if.if.else.if.endif"
.3.else.else.if.if.if.else.if.else:
  %".211" = alloca %"Object"*
  %".212" = load %"Main"*, %"Main"** %".4"
  %".213" = getelementptr inbounds %"Main", %"Main"* %".212", i32 0, i32 1
  %".214" = load i32, i32* %".213"
  %".215" = icmp ult i32 %".214", 8
  br i1 %".215", label %".3.else.else.if.if.if.else.if.else.if", label %".3.else.else.if.if.if.else.if.else.else"
.3.else.else.if.if.if.else.if.endif:
  %".240" = load %"Object"*, %"Object"** %".195"
  store %"Object"* %".240", %"Object"** %".189"
  br label %".3.else.else.if.if.if.else.endif"
.3.else.else.if.if.if.else.if.else.if:
  %".217" = load %"Main"*, %"Main"** %".4"
  %".218" = getelementptr inbounds %"Main", %"Main"* %".217", i32 0, i32 0
  %".219" = load %"MainVT"*, %"MainVT"** %".218"
  %".220" = getelementptr inbounds %"MainVT", %"MainVT"* %".219", i32 0, i32 0
  %".221" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".220"
  %".222" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.11", i32 0, i32 0
  %".223" = bitcast %"Main"* %".217" to %"Object"*
  %".224" = call %"Object"* %".221"(%"Object"* %".223", i8* %".222")
  store %"Object"* %".224", %"Object"** %".211"
  br label %".3.else.else.if.if.if.else.if.else.endif"
.3.else.else.if.if.if.else.if.else.else:
  %".227" = load %"Main"*, %"Main"** %".4"
  %".228" = getelementptr inbounds %"Main", %"Main"* %".227", i32 0, i32 0
  %".229" = load %"MainVT"*, %"MainVT"** %".228"
  %".230" = getelementptr inbounds %"MainVT", %"MainVT"* %".229", i32 0, i32 0
  %".231" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".230"
  %".232" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.12", i32 0, i32 0
  %".233" = bitcast %"Main"* %".227" to %"Object"*
  %".234" = call %"Object"* %".231"(%"Object"* %".233", i8* %".232")
  store %"Object"* %".234", %"Object"** %".211"
  br label %".3.else.else.if.if.if.else.if.else.endif"
.3.else.else.if.if.if.else.if.else.endif:
  %".237" = load %"Object"*, %"Object"** %".211"
  store %"Object"* %".237", %"Object"** %".195"
  br label %".3.else.else.if.if.if.else.if.endif"
.3.else.else.if.if.if.else.else.if:
  %".249" = load %"Main"*, %"Main"** %".4"
  %".250" = getelementptr inbounds %"Main", %"Main"* %".249", i32 0, i32 0
  %".251" = load %"MainVT"*, %"MainVT"** %".250"
  %".252" = getelementptr inbounds %"MainVT", %"MainVT"* %".251", i32 0, i32 0
  %".253" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".252"
  %".254" = getelementptr inbounds [6 x i8], [6 x i8]* @"string.13", i32 0, i32 0
  %".255" = bitcast %"Main"* %".249" to %"Object"*
  %".256" = call %"Object"* %".253"(%"Object"* %".255", i8* %".254")
  store %"Object"* %".256", %"Object"** %".243"
  br label %".3.else.else.if.if.if.else.else.endif"
.3.else.else.if.if.if.else.else.else:
  %".259" = alloca %"Object"*
  %".260" = load %"Main"*, %"Main"** %".4"
  %".261" = getelementptr inbounds %"Main", %"Main"* %".260", i32 0, i32 1
  %".262" = load i32, i32* %".261"
  %".263" = icmp ult i32 %".262", 11
  br i1 %".263", label %".3.else.else.if.if.if.else.else.else.if", label %".3.else.else.if.if.if.else.else.else.else"
.3.else.else.if.if.if.else.else.endif:
  %".288" = load %"Object"*, %"Object"** %".243"
  store %"Object"* %".288", %"Object"** %".189"
  br label %".3.else.else.if.if.if.else.endif"
.3.else.else.if.if.if.else.else.else.if:
  %".265" = load %"Main"*, %"Main"** %".4"
  %".266" = getelementptr inbounds %"Main", %"Main"* %".265", i32 0, i32 0
  %".267" = load %"MainVT"*, %"MainVT"** %".266"
  %".268" = getelementptr inbounds %"MainVT", %"MainVT"* %".267", i32 0, i32 0
  %".269" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".268"
  %".270" = getelementptr inbounds [7 x i8], [7 x i8]* @"string.14", i32 0, i32 0
  %".271" = bitcast %"Main"* %".265" to %"Object"*
  %".272" = call %"Object"* %".269"(%"Object"* %".271", i8* %".270")
  store %"Object"* %".272", %"Object"** %".259"
  br label %".3.else.else.if.if.if.else.else.else.endif"
.3.else.else.if.if.if.else.else.else.else:
  %".275" = load %"Main"*, %"Main"** %".4"
  %".276" = getelementptr inbounds %"Main", %"Main"* %".275", i32 0, i32 0
  %".277" = load %"MainVT"*, %"MainVT"** %".276"
  %".278" = getelementptr inbounds %"MainVT", %"MainVT"* %".277", i32 0, i32 0
  %".279" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".278"
  %".280" = getelementptr inbounds [7 x i8], [7 x i8]* @"string.15", i32 0, i32 0
  %".281" = bitcast %"Main"* %".275" to %"Object"*
  %".282" = call %"Object"* %".279"(%"Object"* %".281", i8* %".280")
  store %"Object"* %".282", %"Object"** %".259"
  br label %".3.else.else.if.if.if.else.else.else.endif"
.3.else.else.if.if.if.else.else.else.endif:
  %".285" = load %"Object"*, %"Object"** %".259"
  store %"Object"* %".285", %"Object"** %".243"
  br label %".3.else.else.if.if.if.else.else.endif"
}

define i32 @"main"(%"Main"* %".1") 
{
.3:
  %".4" = call %"Main"* @"Main___new"()
  %".5" = alloca %"Main"*
  store %"Main"* %".4", %"Main"** %".5"
  %".7" = load %"Main"*, %"Main"** %".5"
  %".8" = getelementptr inbounds %"Main", %"Main"* %".7", i32 0, i32 0
  %".9" = load %"MainVT"*, %"MainVT"** %".8"
  %".10" = getelementptr inbounds %"MainVT", %"MainVT"* %".9", i32 0, i32 6
  %".11" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".10"
  %".12" = call i1 %".11"(%"Main"* %".7")
  %".13" = load %"Main"*, %"Main"** %".5"
  %".14" = getelementptr inbounds %"Main", %"Main"* %".13", i32 0, i32 1
  store i32 1, i32* %".14"
  %".16" = load %"Main"*, %"Main"** %".5"
  %".17" = getelementptr inbounds %"Main", %"Main"* %".16", i32 0, i32 0
  %".18" = load %"MainVT"*, %"MainVT"** %".17"
  %".19" = getelementptr inbounds %"MainVT", %"MainVT"* %".18", i32 0, i32 6
  %".20" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".19"
  %".21" = call i1 %".20"(%"Main"* %".16")
  %".22" = load %"Main"*, %"Main"** %".5"
  %".23" = getelementptr inbounds %"Main", %"Main"* %".22", i32 0, i32 1
  store i32 2, i32* %".23"
  %".25" = load %"Main"*, %"Main"** %".5"
  %".26" = getelementptr inbounds %"Main", %"Main"* %".25", i32 0, i32 0
  %".27" = load %"MainVT"*, %"MainVT"** %".26"
  %".28" = getelementptr inbounds %"MainVT", %"MainVT"* %".27", i32 0, i32 6
  %".29" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".28"
  %".30" = call i1 %".29"(%"Main"* %".25")
  %".31" = load %"Main"*, %"Main"** %".5"
  %".32" = getelementptr inbounds %"Main", %"Main"* %".31", i32 0, i32 1
  store i32 4, i32* %".32"
  %".34" = load %"Main"*, %"Main"** %".5"
  %".35" = getelementptr inbounds %"Main", %"Main"* %".34", i32 0, i32 0
  %".36" = load %"MainVT"*, %"MainVT"** %".35"
  %".37" = getelementptr inbounds %"MainVT", %"MainVT"* %".36", i32 0, i32 6
  %".38" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".37"
  %".39" = call i1 %".38"(%"Main"* %".34")
  %".40" = load %"Main"*, %"Main"** %".5"
  %".41" = getelementptr inbounds %"Main", %"Main"* %".40", i32 0, i32 1
  store i32 8, i32* %".41"
  %".43" = load %"Main"*, %"Main"** %".5"
  %".44" = getelementptr inbounds %"Main", %"Main"* %".43", i32 0, i32 0
  %".45" = load %"MainVT"*, %"MainVT"** %".44"
  %".46" = getelementptr inbounds %"MainVT", %"MainVT"* %".45", i32 0, i32 6
  %".47" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".46"
  %".48" = call i1 %".47"(%"Main"* %".43")
  %".49" = load %"Main"*, %"Main"** %".5"
  %".50" = getelementptr inbounds %"Main", %"Main"* %".49", i32 0, i32 1
  store i32 16, i32* %".50"
  %".52" = load %"Main"*, %"Main"** %".5"
  %".53" = getelementptr inbounds %"Main", %"Main"* %".52", i32 0, i32 0
  %".54" = load %"MainVT"*, %"MainVT"** %".53"
  %".55" = getelementptr inbounds %"MainVT", %"MainVT"* %".54", i32 0, i32 6
  %".56" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".55"
  %".57" = call i1 %".56"(%"Main"* %".52")
  %".58" = load %"Main"*, %"Main"** %".5"
  %".59" = getelementptr inbounds %"Main", %"Main"* %".58", i32 0, i32 1
  store i32 32, i32* %".59"
  %".61" = load %"Main"*, %"Main"** %".5"
  %".62" = getelementptr inbounds %"Main", %"Main"* %".61", i32 0, i32 0
  %".63" = load %"MainVT"*, %"MainVT"** %".62"
  %".64" = getelementptr inbounds %"MainVT", %"MainVT"* %".63", i32 0, i32 6
  %".65" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".64"
  %".66" = call i1 %".65"(%"Main"* %".61")
  %".67" = load %"Main"*, %"Main"** %".5"
  %".68" = getelementptr inbounds %"Main", %"Main"* %".67", i32 0, i32 1
  store i32 64, i32* %".68"
  %".70" = load %"Main"*, %"Main"** %".5"
  %".71" = getelementptr inbounds %"Main", %"Main"* %".70", i32 0, i32 0
  %".72" = load %"MainVT"*, %"MainVT"** %".71"
  %".73" = getelementptr inbounds %"MainVT", %"MainVT"* %".72", i32 0, i32 6
  %".74" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".73"
  %".75" = call i1 %".74"(%"Main"* %".70")
  %".76" = load %"Main"*, %"Main"** %".5"
  %".77" = getelementptr inbounds %"Main", %"Main"* %".76", i32 0, i32 1
  store i32 128, i32* %".77"
  %".79" = load %"Main"*, %"Main"** %".5"
  %".80" = getelementptr inbounds %"Main", %"Main"* %".79", i32 0, i32 0
  %".81" = load %"MainVT"*, %"MainVT"** %".80"
  %".82" = getelementptr inbounds %"MainVT", %"MainVT"* %".81", i32 0, i32 6
  %".83" = load i1 (%"Main"*)*, i1 (%"Main"*)** %".82"
  %".84" = call i1 %".83"(%"Main"* %".79")
  ret i32 0
}

define %"Main"* @"Main___new"() 
{
.2:
  %"size_ptr" = getelementptr %"Main", %"Main"* null, i32 1
  %"size_i64" = ptrtoint %"Main"* %"size_ptr" to i64
  %".3" = call i8* @"malloc"(i64 %"size_i64")
  %".4" = bitcast i8* %".3" to %"Main"*
  %".5" = call %"Main"* @"Main___init"(%"Main"* %".4")
  ret %"Main"* %".5"
}

define %"Main"* @"Main___init"(%"Main"* %".1") 
{
.3:
  %".4" = icmp ne %"Main"* %".1", null
  br i1 %".4", label %".3.if", label %".3.endif"
.3.if:
  %".6" = bitcast %"Main"* %".1" to %"Object"*
  %".7" = call %"Object"* @"Object___init"(%"Object"* %".6")
  %".8" = getelementptr inbounds %"Main", %"Main"* %".1", i32 0, i32 0
  store %"MainVT"* @"MainVT", %"MainVT"** %".8"
  %".10" = getelementptr %"Main", %"Main"* %".1", i32 0, i32 1
  store i32 0, i32* %".10"
  br label %".3.endif"
.3.endif:
  ret %"Main"* %".1"
}

@"MainVT" = constant %"MainVT" {%"Object"* (%"Object"*, i8*)* @"Object__print", %"Object"* (%"Object"*, i1)* @"Object__printBool", %"Object"* (%"Object"*, i32)* @"Object__printInt32", i8* (%"Object"*)* @"Object__inputLine", i1 (%"Object"*)* @"Object__inputBool", i32 (%"Object"*)* @"Object__inputInt32", i1 (%"Main"*)* @"Main__guessN", i32 (%"Main"*)* @"main"}
@"string" = constant [5 x i8] c"n = \00"
@"string.1" = constant [12 x i8] c", guess is \00"
@"string.2" = constant [6 x i8] c"n < 0\00"
@"string.3" = constant [8 x i8] c"n > 100\00"
@"string.4" = constant [6 x i8] c"n = 0\00"
@"string.5" = constant [6 x i8] c"n = 1\00"
@"string.6" = constant [6 x i8] c"n = 2\00"
@"string.7" = constant [6 x i8] c"n = 3\00"
@"string.8" = constant [6 x i8] c"n = 4\00"
@"string.9" = constant [6 x i8] c"n = 5\00"
@"string.10" = constant [6 x i8] c"n = 6\00"
@"string.11" = constant [6 x i8] c"n = 7\00"
@"string.12" = constant [6 x i8] c"n = 8\00"
@"string.13" = constant [6 x i8] c"n = 9\00"
@"string.14" = constant [7 x i8] c"n = 10\00"
@"string.15" = constant [7 x i8] c"n = 11\00"
@"string.16" = constant [13 x i8] c"12 <= n < 25\00"
@"string.17" = constant [13 x i8] c"25 <= n < 50\00"
@"string.18" = constant [15 x i8] c"50 <= n <= 100\00"
@"string.19" = constant [2 x i8] c"\0a\00"