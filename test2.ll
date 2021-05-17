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



%"Main" = type {%"MainVT"*}
%"MainVT" = type {%"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i1)*, %"Object"* (%"Object"*, i32)*, i8* (%"Object"*)*, i1 (%"Object"*)*, i32 (%"Object"*)*, i32 (%"Main"*)*}
define i32 @"main"(%"Main"* %".1") 
{
.3:
  %".4" = call %"Main"* @"Main___new"()
  %".5" = alloca %"Main"*
  store %"Main"* %".4", %"Main"** %".5"
  %".7" = alloca %"Object"*
  %".8" = alloca i1
  %".9" = load %"Main"*, %"Main"** %".5"
  %".10" = getelementptr inbounds %"Main", %"Main"* %".9", i32 0, i32 0
  %".11" = load %"MainVT"*, %"MainVT"** %".10"
  %".12" = getelementptr inbounds %"MainVT", %"MainVT"* %".11", i32 0, i32 0
  %".13" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".12"
  %".14" = getelementptr inbounds [4 x i8], [4 x i8]* @"string", i32 0, i32 0
  %".15" = bitcast %"Main"* %".9" to %"Object"*
  %".16" = call %"Object"* %".13"(%"Object"* %".15", i8* %".14")
  store i1 1, i1* %".8"
  br i1 1, label %"add_cond", label %"add_exit"
add_exit:
  %".29" = load i1, i1* %".8"
  br i1 %".29", label %"add_exit.if", label %"add_exit.else"
add_cond:
  %".19" = load %"Main"*, %"Main"** %".5"
  %".20" = getelementptr inbounds %"Main", %"Main"* %".19", i32 0, i32 0
  %".21" = load %"MainVT"*, %"MainVT"** %".20"
  %".22" = getelementptr inbounds %"MainVT", %"MainVT"* %".21", i32 0, i32 0
  %".23" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".22"
  %".24" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.1", i32 0, i32 0
  %".25" = bitcast %"Main"* %".19" to %"Object"*
  %".26" = call %"Object"* %".23"(%"Object"* %".25", i8* %".24")
  store i1 1, i1* %".8"
  br label %"add_exit"
add_exit.if:
  %".31" = load %"Main"*, %"Main"** %".5"
  %".32" = getelementptr inbounds %"Main", %"Main"* %".31", i32 0, i32 0
  %".33" = load %"MainVT"*, %"MainVT"** %".32"
  %".34" = getelementptr inbounds %"MainVT", %"MainVT"* %".33", i32 0, i32 0
  %".35" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".34"
  %".36" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.2", i32 0, i32 0
  %".37" = bitcast %"Main"* %".31" to %"Object"*
  %".38" = call %"Object"* %".35"(%"Object"* %".37", i8* %".36")
  store %"Object"* %".38", %"Object"** %".7"
  br label %"add_exit.endif"
add_exit.else:
  %".41" = load %"Main"*, %"Main"** %".5"
  %".42" = getelementptr inbounds %"Main", %"Main"* %".41", i32 0, i32 0
  %".43" = load %"MainVT"*, %"MainVT"** %".42"
  %".44" = getelementptr inbounds %"MainVT", %"MainVT"* %".43", i32 0, i32 0
  %".45" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".44"
  %".46" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.3", i32 0, i32 0
  %".47" = bitcast %"Main"* %".41" to %"Object"*
  %".48" = call %"Object"* %".45"(%"Object"* %".47", i8* %".46")
  store %"Object"* %".48", %"Object"** %".7"
  br label %"add_exit.endif"
add_exit.endif:
  %".51" = load %"Object"*, %"Object"** %".7"
  %".52" = alloca %"Object"*
  %".53" = alloca i1
  %".54" = load %"Main"*, %"Main"** %".5"
  %".55" = getelementptr inbounds %"Main", %"Main"* %".54", i32 0, i32 0
  %".56" = load %"MainVT"*, %"MainVT"** %".55"
  %".57" = getelementptr inbounds %"MainVT", %"MainVT"* %".56", i32 0, i32 0
  %".58" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".57"
  %".59" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.4", i32 0, i32 0
  %".60" = bitcast %"Main"* %".54" to %"Object"*
  %".61" = call %"Object"* %".58"(%"Object"* %".60", i8* %".59")
  store i1 1, i1* %".53"
  br i1 1, label %"add_cond.1", label %"add_exit.1"
add_exit.1:
  %".74" = load i1, i1* %".53"
  br i1 %".74", label %"add_exit.1.if", label %"add_exit.1.else"
add_cond.1:
  %".64" = load %"Main"*, %"Main"** %".5"
  %".65" = getelementptr inbounds %"Main", %"Main"* %".64", i32 0, i32 0
  %".66" = load %"MainVT"*, %"MainVT"** %".65"
  %".67" = getelementptr inbounds %"MainVT", %"MainVT"* %".66", i32 0, i32 0
  %".68" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".67"
  %".69" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.5", i32 0, i32 0
  %".70" = bitcast %"Main"* %".64" to %"Object"*
  %".71" = call %"Object"* %".68"(%"Object"* %".70", i8* %".69")
  store i1 0, i1* %".53"
  br label %"add_exit.1"
add_exit.1.if:
  %".76" = load %"Main"*, %"Main"** %".5"
  %".77" = getelementptr inbounds %"Main", %"Main"* %".76", i32 0, i32 0
  %".78" = load %"MainVT"*, %"MainVT"** %".77"
  %".79" = getelementptr inbounds %"MainVT", %"MainVT"* %".78", i32 0, i32 0
  %".80" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".79"
  %".81" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.6", i32 0, i32 0
  %".82" = bitcast %"Main"* %".76" to %"Object"*
  %".83" = call %"Object"* %".80"(%"Object"* %".82", i8* %".81")
  store %"Object"* %".83", %"Object"** %".52"
  br label %"add_exit.1.endif"
add_exit.1.else:
  %".86" = load %"Main"*, %"Main"** %".5"
  %".87" = getelementptr inbounds %"Main", %"Main"* %".86", i32 0, i32 0
  %".88" = load %"MainVT"*, %"MainVT"** %".87"
  %".89" = getelementptr inbounds %"MainVT", %"MainVT"* %".88", i32 0, i32 0
  %".90" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".89"
  %".91" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.7", i32 0, i32 0
  %".92" = bitcast %"Main"* %".86" to %"Object"*
  %".93" = call %"Object"* %".90"(%"Object"* %".92", i8* %".91")
  store %"Object"* %".93", %"Object"** %".52"
  br label %"add_exit.1.endif"
add_exit.1.endif:
  %".96" = load %"Object"*, %"Object"** %".52"
  %".97" = alloca %"Object"*
  %".98" = alloca i1
  %".99" = load %"Main"*, %"Main"** %".5"
  %".100" = getelementptr inbounds %"Main", %"Main"* %".99", i32 0, i32 0
  %".101" = load %"MainVT"*, %"MainVT"** %".100"
  %".102" = getelementptr inbounds %"MainVT", %"MainVT"* %".101", i32 0, i32 0
  %".103" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".102"
  %".104" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.8", i32 0, i32 0
  %".105" = bitcast %"Main"* %".99" to %"Object"*
  %".106" = call %"Object"* %".103"(%"Object"* %".105", i8* %".104")
  store i1 0, i1* %".98"
  br i1 0, label %"add_cond.2", label %"add_exit.2"
add_exit.2:
  %".119" = load i1, i1* %".98"
  br i1 %".119", label %"add_exit.2.if", label %"add_exit.2.else"
add_cond.2:
  %".109" = load %"Main"*, %"Main"** %".5"
  %".110" = getelementptr inbounds %"Main", %"Main"* %".109", i32 0, i32 0
  %".111" = load %"MainVT"*, %"MainVT"** %".110"
  %".112" = getelementptr inbounds %"MainVT", %"MainVT"* %".111", i32 0, i32 0
  %".113" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".112"
  %".114" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.9", i32 0, i32 0
  %".115" = bitcast %"Main"* %".109" to %"Object"*
  %".116" = call %"Object"* %".113"(%"Object"* %".115", i8* %".114")
  store i1 1, i1* %".98"
  br label %"add_exit.2"
add_exit.2.if:
  %".121" = load %"Main"*, %"Main"** %".5"
  %".122" = getelementptr inbounds %"Main", %"Main"* %".121", i32 0, i32 0
  %".123" = load %"MainVT"*, %"MainVT"** %".122"
  %".124" = getelementptr inbounds %"MainVT", %"MainVT"* %".123", i32 0, i32 0
  %".125" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".124"
  %".126" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.10", i32 0, i32 0
  %".127" = bitcast %"Main"* %".121" to %"Object"*
  %".128" = call %"Object"* %".125"(%"Object"* %".127", i8* %".126")
  store %"Object"* %".128", %"Object"** %".97"
  br label %"add_exit.2.endif"
add_exit.2.else:
  %".131" = load %"Main"*, %"Main"** %".5"
  %".132" = getelementptr inbounds %"Main", %"Main"* %".131", i32 0, i32 0
  %".133" = load %"MainVT"*, %"MainVT"** %".132"
  %".134" = getelementptr inbounds %"MainVT", %"MainVT"* %".133", i32 0, i32 0
  %".135" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".134"
  %".136" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.11", i32 0, i32 0
  %".137" = bitcast %"Main"* %".131" to %"Object"*
  %".138" = call %"Object"* %".135"(%"Object"* %".137", i8* %".136")
  store %"Object"* %".138", %"Object"** %".97"
  br label %"add_exit.2.endif"
add_exit.2.endif:
  %".141" = load %"Object"*, %"Object"** %".97"
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
  store %"MainVT"* @"Main_vtable", %"MainVT"** %".8"
  br label %".3.endif"
.3.endif:
  ret %"Main"* %".1"
}

@"Main_vtable" = constant %"MainVT" {%"Object"* (%"Object"*, i8*)* @"Object__print", %"Object"* (%"Object"*, i1)* @"Object__printBool", %"Object"* (%"Object"*, i32)* @"Object__printInt32", i8* (%"Object"*)* @"Object__inputLine", i1 (%"Object"*)* @"Object__inputBool", i32 (%"Object"*)* @"Object__inputInt32", i32 (%"Main"*)* @"main"}
@"string" = constant [4 x i8] c"OK\0a\00"
@"string.1" = constant [4 x i8] c"OK\0a\00"
@"string.2" = constant [4 x i8] c"OK\0a\00"
@"string.3" = constant [4 x i8] c"KO\0a\00"
@"string.4" = constant [4 x i8] c"OK\0a\00"
@"string.5" = constant [4 x i8] c"OK\0a\00"
@"string.6" = constant [4 x i8] c"KO\0a\00"
@"string.7" = constant [4 x i8] c"OK\0a\00"
@"string.8" = constant [4 x i8] c"OK\0a\00"
@"string.9" = constant [4 x i8] c"KO\0a\00"
@"string.10" = constant [4 x i8] c"KO\0a\00"
@"string.11" = constant [4 x i8] c"OK\0a\00"