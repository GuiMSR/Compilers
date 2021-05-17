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
  %".8" = load %"Main"*, %"Main"** %".5"
  %".9" = bitcast %"Main"* %".8" to %"Object"*
  %".10" = load %"Main"*, %"Main"** %".5"
  %".11" = bitcast %"Main"* %".10" to %"Object"*
  %".12" = icmp eq %"Object"* %".9", %".11"
  br i1 %".12", label %".3.if", label %".3.else"
.3.if:
  %".14" = load %"Main"*, %"Main"** %".5"
  %".15" = getelementptr inbounds %"Main", %"Main"* %".14", i32 0, i32 0
  %".16" = load %"MainVT"*, %"MainVT"** %".15"
  %".17" = getelementptr inbounds %"MainVT", %"MainVT"* %".16", i32 0, i32 0
  %".18" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".17"
  %".19" = getelementptr inbounds [4 x i8], [4 x i8]* @"string", i32 0, i32 0
  %".20" = bitcast %"Main"* %".14" to %"Object"*
  %".21" = call %"Object"* %".18"(%"Object"* %".20", i8* %".19")
  store %"Object"* %".21", %"Object"** %".7"
  br label %".3.endif"
.3.else:
  %".24" = load %"Main"*, %"Main"** %".5"
  %".25" = getelementptr inbounds %"Main", %"Main"* %".24", i32 0, i32 0
  %".26" = load %"MainVT"*, %"MainVT"** %".25"
  %".27" = getelementptr inbounds %"MainVT", %"MainVT"* %".26", i32 0, i32 0
  %".28" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".27"
  %".29" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.1", i32 0, i32 0
  %".30" = bitcast %"Main"* %".24" to %"Object"*
  %".31" = call %"Object"* %".28"(%"Object"* %".30", i8* %".29")
  store %"Object"* %".31", %"Object"** %".7"
  br label %".3.endif"
.3.endif:
  %".34" = load %"Object"*, %"Object"** %".7"
  %".35" = alloca %"Object"*
  %".36" = load %"Main"*, %"Main"** %".5"
  %".37" = bitcast %"Main"* %".36" to %"Object"*
  %".38" = call %"Main"* @"Main___new"()
  %".39" = bitcast %"Main"* %".38" to %"Object"*
  %".40" = icmp eq %"Object"* %".37", %".39"
  br i1 %".40", label %".3.endif.if", label %".3.endif.else"
.3.endif.if:
  %".42" = load %"Main"*, %"Main"** %".5"
  %".43" = getelementptr inbounds %"Main", %"Main"* %".42", i32 0, i32 0
  %".44" = load %"MainVT"*, %"MainVT"** %".43"
  %".45" = getelementptr inbounds %"MainVT", %"MainVT"* %".44", i32 0, i32 0
  %".46" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".45"
  %".47" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.2", i32 0, i32 0
  %".48" = bitcast %"Main"* %".42" to %"Object"*
  %".49" = call %"Object"* %".46"(%"Object"* %".48", i8* %".47")
  store %"Object"* %".49", %"Object"** %".35"
  br label %".3.endif.endif"
.3.endif.else:
  %".52" = load %"Main"*, %"Main"** %".5"
  %".53" = getelementptr inbounds %"Main", %"Main"* %".52", i32 0, i32 0
  %".54" = load %"MainVT"*, %"MainVT"** %".53"
  %".55" = getelementptr inbounds %"MainVT", %"MainVT"* %".54", i32 0, i32 0
  %".56" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".55"
  %".57" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.3", i32 0, i32 0
  %".58" = bitcast %"Main"* %".52" to %"Object"*
  %".59" = call %"Object"* %".56"(%"Object"* %".58", i8* %".57")
  store %"Object"* %".59", %"Object"** %".35"
  br label %".3.endif.endif"
.3.endif.endif:
  %".62" = load %"Object"*, %"Object"** %".35"
  %".63" = alloca %"Object"*
  store %"Object"* null, %"Object"** %".63"
  %".65" = alloca %"Object"*
  %".66" = load %"Object"*, %"Object"** %".63"
  %".67" = load %"Main"*, %"Main"** %".5"
  %".68" = bitcast %"Main"* %".67" to %"Object"*
  %".69" = icmp eq %"Object"* %".66", %".68"
  br i1 %".69", label %".3.endif.endif.if", label %".3.endif.endif.else"
.3.endif.endif.if:
  %".71" = load %"Main"*, %"Main"** %".5"
  %".72" = getelementptr inbounds %"Main", %"Main"* %".71", i32 0, i32 0
  %".73" = load %"MainVT"*, %"MainVT"** %".72"
  %".74" = getelementptr inbounds %"MainVT", %"MainVT"* %".73", i32 0, i32 0
  %".75" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".74"
  %".76" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.4", i32 0, i32 0
  %".77" = bitcast %"Main"* %".71" to %"Object"*
  %".78" = call %"Object"* %".75"(%"Object"* %".77", i8* %".76")
  store %"Object"* %".78", %"Object"** %".65"
  br label %".3.endif.endif.endif"
.3.endif.endif.else:
  %".81" = load %"Main"*, %"Main"** %".5"
  %".82" = getelementptr inbounds %"Main", %"Main"* %".81", i32 0, i32 0
  %".83" = load %"MainVT"*, %"MainVT"** %".82"
  %".84" = getelementptr inbounds %"MainVT", %"MainVT"* %".83", i32 0, i32 0
  %".85" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".84"
  %".86" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.5", i32 0, i32 0
  %".87" = bitcast %"Main"* %".81" to %"Object"*
  %".88" = call %"Object"* %".85"(%"Object"* %".87", i8* %".86")
  store %"Object"* %".88", %"Object"** %".65"
  br label %".3.endif.endif.endif"
.3.endif.endif.endif:
  %".91" = load %"Object"*, %"Object"** %".65"
  %".92" = alloca %"Object"*
  %".93" = load %"Main"*, %"Main"** %".5"
  %".94" = bitcast %"Main"* %".93" to %"Object"*
  %".95" = load %"Object"*, %"Object"** %".63"
  %".96" = icmp eq %"Object"* %".94", %".95"
  br i1 %".96", label %".3.endif.endif.endif.if", label %".3.endif.endif.endif.else"
.3.endif.endif.endif.if:
  %".98" = load %"Main"*, %"Main"** %".5"
  %".99" = getelementptr inbounds %"Main", %"Main"* %".98", i32 0, i32 0
  %".100" = load %"MainVT"*, %"MainVT"** %".99"
  %".101" = getelementptr inbounds %"MainVT", %"MainVT"* %".100", i32 0, i32 0
  %".102" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".101"
  %".103" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.6", i32 0, i32 0
  %".104" = bitcast %"Main"* %".98" to %"Object"*
  %".105" = call %"Object"* %".102"(%"Object"* %".104", i8* %".103")
  store %"Object"* %".105", %"Object"** %".92"
  br label %".3.endif.endif.endif.endif"
.3.endif.endif.endif.else:
  %".108" = load %"Main"*, %"Main"** %".5"
  %".109" = getelementptr inbounds %"Main", %"Main"* %".108", i32 0, i32 0
  %".110" = load %"MainVT"*, %"MainVT"** %".109"
  %".111" = getelementptr inbounds %"MainVT", %"MainVT"* %".110", i32 0, i32 0
  %".112" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".111"
  %".113" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.7", i32 0, i32 0
  %".114" = bitcast %"Main"* %".108" to %"Object"*
  %".115" = call %"Object"* %".112"(%"Object"* %".114", i8* %".113")
  store %"Object"* %".115", %"Object"** %".92"
  br label %".3.endif.endif.endif.endif"
.3.endif.endif.endif.endif:
  %".118" = load %"Object"*, %"Object"** %".92"
  %".119" = load %"Main"*, %"Main"** %".5"
  %".120" = bitcast %"Main"* %".119" to %"Object"*
  store %"Object"* %".120", %"Object"** %".63"
  %".122" = alloca %"Object"*
  %".123" = load %"Object"*, %"Object"** %".63"
  %".124" = load %"Main"*, %"Main"** %".5"
  %".125" = bitcast %"Main"* %".124" to %"Object"*
  %".126" = icmp eq %"Object"* %".123", %".125"
  br i1 %".126", label %".3.endif.endif.endif.endif.if", label %".3.endif.endif.endif.endif.else"
.3.endif.endif.endif.endif.if:
  %".128" = load %"Main"*, %"Main"** %".5"
  %".129" = getelementptr inbounds %"Main", %"Main"* %".128", i32 0, i32 0
  %".130" = load %"MainVT"*, %"MainVT"** %".129"
  %".131" = getelementptr inbounds %"MainVT", %"MainVT"* %".130", i32 0, i32 0
  %".132" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".131"
  %".133" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.8", i32 0, i32 0
  %".134" = bitcast %"Main"* %".128" to %"Object"*
  %".135" = call %"Object"* %".132"(%"Object"* %".134", i8* %".133")
  store %"Object"* %".135", %"Object"** %".122"
  br label %".3.endif.endif.endif.endif.endif"
.3.endif.endif.endif.endif.else:
  %".138" = load %"Main"*, %"Main"** %".5"
  %".139" = getelementptr inbounds %"Main", %"Main"* %".138", i32 0, i32 0
  %".140" = load %"MainVT"*, %"MainVT"** %".139"
  %".141" = getelementptr inbounds %"MainVT", %"MainVT"* %".140", i32 0, i32 0
  %".142" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".141"
  %".143" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.9", i32 0, i32 0
  %".144" = bitcast %"Main"* %".138" to %"Object"*
  %".145" = call %"Object"* %".142"(%"Object"* %".144", i8* %".143")
  store %"Object"* %".145", %"Object"** %".122"
  br label %".3.endif.endif.endif.endif.endif"
.3.endif.endif.endif.endif.endif:
  %".148" = load %"Object"*, %"Object"** %".122"
  %".149" = alloca %"Object"*
  %".150" = load %"Main"*, %"Main"** %".5"
  %".151" = bitcast %"Main"* %".150" to %"Object"*
  %".152" = load %"Object"*, %"Object"** %".63"
  %".153" = icmp eq %"Object"* %".151", %".152"
  br i1 %".153", label %".3.endif.endif.endif.endif.endif.if", label %".3.endif.endif.endif.endif.endif.else"
.3.endif.endif.endif.endif.endif.if:
  %".155" = load %"Main"*, %"Main"** %".5"
  %".156" = getelementptr inbounds %"Main", %"Main"* %".155", i32 0, i32 0
  %".157" = load %"MainVT"*, %"MainVT"** %".156"
  %".158" = getelementptr inbounds %"MainVT", %"MainVT"* %".157", i32 0, i32 0
  %".159" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".158"
  %".160" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.10", i32 0, i32 0
  %".161" = bitcast %"Main"* %".155" to %"Object"*
  %".162" = call %"Object"* %".159"(%"Object"* %".161", i8* %".160")
  store %"Object"* %".162", %"Object"** %".149"
  br label %".3.endif.endif.endif.endif.endif.endif"
.3.endif.endif.endif.endif.endif.else:
  %".165" = load %"Main"*, %"Main"** %".5"
  %".166" = getelementptr inbounds %"Main", %"Main"* %".165", i32 0, i32 0
  %".167" = load %"MainVT"*, %"MainVT"** %".166"
  %".168" = getelementptr inbounds %"MainVT", %"MainVT"* %".167", i32 0, i32 0
  %".169" = load %"Object"* (%"Object"*, i8*)*, %"Object"* (%"Object"*, i8*)** %".168"
  %".170" = getelementptr inbounds [4 x i8], [4 x i8]* @"string.11", i32 0, i32 0
  %".171" = bitcast %"Main"* %".165" to %"Object"*
  %".172" = call %"Object"* %".169"(%"Object"* %".171", i8* %".170")
  store %"Object"* %".172", %"Object"** %".149"
  br label %".3.endif.endif.endif.endif.endif.endif"
.3.endif.endif.endif.endif.endif.endif:
  %".175" = load %"Object"*, %"Object"** %".149"
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
@"string.1" = constant [4 x i8] c"KO\0a\00"
@"string.2" = constant [4 x i8] c"KO\0a\00"
@"string.3" = constant [4 x i8] c"OK\0a\00"
@"string.4" = constant [4 x i8] c"KO\0a\00"
@"string.5" = constant [4 x i8] c"OK\0a\00"
@"string.6" = constant [4 x i8] c"KO\0a\00"
@"string.7" = constant [4 x i8] c"OK\0a\00"
@"string.8" = constant [4 x i8] c"OK\0a\00"
@"string.9" = constant [4 x i8] c"KO\0a\00"
@"string.10" = constant [4 x i8] c"OK\0a\00"
@"string.11" = constant [4 x i8] c"KO\0a\00"