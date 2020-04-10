#include <jni.h> 
#include <stdio.h> 
#include "Utility.h" 
JNIEXPORT void JNICALL Java_Utility_divide(JNIEnv *env, jobject obj) { 
	float a,b,c;
	printf("\n****Called Divide Module from C language****\n"); 
	printf("Enter numbers to Divide: "); 
	scanf("%f %f",&a,&b); 
	c = a/b;
	printf("Division of %f and %f is %f\n",a,b,c);
	return; 
}