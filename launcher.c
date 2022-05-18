#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>
#include <stdbool.h> 
int x;
int relaunch(){
	int i = fork();
	if(i==0){
		execlp("python","python","main.py",NULL);
		exit(0);
	}else{
		return i;
	}


}
void handler(int z){
	kill(x, SIGKILL);
	wait(&x);
	printf("[LAUNCHER] : NOTE : Cleaned up loose ends from dirty exit... exiting\n ");
	exit(0);
}
int main(int argc, char** argv){
	struct sigaction act;
	act.sa_handler = handler;
    	sigaction(SIGINT, &act, NULL);
	printf("[LAUNCHER] : NOTE : Launcher is starting main.py\n");
	printf("[LAUNCHER] : NOTE : Logs from Laucher are not recorded in main.log\n");
	x = relaunch();
	while(1){
		wait(&x);
		if(argc>1){
			printf("[LAUNCHER] : NOTE: main is dead, relaunching\n");
		}else{
			printf("[LAUNCHER] : NOTE: main is dead, relaunch disabled... exiting...\n");
			exit(0);
		}
	}
}
