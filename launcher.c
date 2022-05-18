#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>
#include <stdbool.h> 
#include <linux/reboot.h>
int x;
int reboot(int);
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
	kill(x, SIGINT); // Pass sigint to python so it shuts down clean
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
		int status=0;
		wait(&status);
		if(WEXITSTATUS(status)==1){
			printf("[LAUNCHER] : Severe error detected... not relaunching\n");
			exit(1);
		}else if(WEXITSTATUS(status)==99){
			printf("[LAUNCHER] : NOTE: Main returned with 'relaunch' status\n");
		}else if(WEXITSTATUS(status)==100){
			sleep(3);
			printf("[LAUNCHER] : NOTE : Reboot requested...");
			reboot(LINUX_REBOOT_CMD_RESTART);
		}else{
			printf("[LAUNCHER] : python returned with unknown error: %d\n relaunching...\n",WEXITSTATUS(status));
		}
		if(argc>1){
			printf("[LAUNCHER] : NOTE: main is dead, relaunching\n");
			x = relaunch();

		}else{
			printf("[LAUNCHER] : NOTE: main is dead, relaunch disabled... exiting...\n");
			exit(0);
		}
	}
}
