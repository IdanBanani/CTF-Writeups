//#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include "kd_def.h"
typedef struct
{
    unsigned char key[16];
    int key_index;
    unsigned char second_flag[24];
} gametype;

gametype gamestate; //global
unsigned int rndindex2 = 0; //global

typedef struct rc2_key_st
{
    unsigned short xkey[64];
} RC2_Schedule;

 unsigned char  rndtable[256] = 
      {0, 8, 109, 220, 222, 241, 149, 107,  75, 248, 254, 140,  16,  66,
      74,  21, 211,  47,  80, 242, 154,  27, 205, 128, 161,  89,  77,  36,
      95, 110,  85,  48, 212, 140, 211, 249,  22,  79, 200,  50,  28, 188,
      52, 140, 202, 120,  68, 145,  62,  70, 184, 190,  91, 197, 152, 224,
      149, 104,  25, 178, 252, 182, 202, 182, 141, 197,   4,  81, 181, 242,
      145,  42,  39, 227, 156, 198, 225, 193, 219,  93, 122, 175, 249,   0,
      175, 143,  70, 239,  46, 246, 163,  53, 163, 109, 168, 135,   2, 235,
       25,  92,  20, 145, 138,  77,  69, 166,  78, 176, 173, 212, 166, 113,
       94, 161,  41,  50, 239,  49, 111, 164,  70,  60,   2,  37, 171,  75,
      136, 156,  11,  56,  42, 146, 138, 229,  73, 146,  77,  61,  98, 196,
      135, 106,  63, 197, 195,  86,  96, 203, 113, 101, 170, 247, 181, 113,
       80, 250, 108,   7, 255, 237, 129, 226,  79, 107, 112, 166, 103, 241,
       24, 223, 239, 120, 198,  58,  60,  82, 128,   3, 184,  66, 143, 224,
      145, 224,  81, 206, 163,  45,  63,  90, 168, 114,  59,  33, 159,  95,
       28, 139, 123,  98, 125, 196,  15,  70, 194, 253,  54,  14, 109, 226,
       71,  17, 161,  93, 186,  87, 244, 138,  20,  52, 123, 251,  26,  36,
       17,  46,  52, 231, 232,  76,  31, 221,  84,  37, 216, 165, 212, 106,
      197, 242,  98,  43,  39, 175, 254, 145, 190,  84, 118, 222, 187, 136,
      120, 163, 236, 249};


void rc2_decrypt(const RC2_Schedule* key_schedule,
    unsigned char* plain,
    const unsigned char* cipher)
{
    unsigned x76, x54, x32, x10, i;
    x76 = (cipher[7] << 8) + cipher[6];
    x54 = (cipher[5] << 8) + cipher[4];
    x32 = (cipher[3] << 8) + cipher[2];
    x10 = (cipher[1] << 8) + cipher[0];
    i = 15;
    do
    {
        x76 &= 65535;
        x76 = (x76 << 11) + (x76 >> 5);
        x76 -= (x10 & ~x54) + (x32 & x54) + key_schedule->xkey[4 * i + 3];
        x54 &= 65535;
        x54 = (x54 << 13) + (x54 >> 3);
        x54 -= (x76 & ~x32) + (x10 & x32) + key_schedule->xkey[4 * i + 2];
        x32 &= 65535;
        x32 = (x32 << 14) + (x32 >> 2);
        x32 -= (x54 & ~x10) + (x76 & x10) + key_schedule->xkey[4 * i + 1];
        x10 &= 65535;
        x10 = (x10 << 15) + (x10 >> 1);
        x10 -= (x32 & ~x76) + (x54 & x76) + key_schedule->xkey[4 * i + 0];
        if (i == 5 || i == 11)
        {
            x76 -= key_schedule->xkey[x54 & 63];
            x54 -= key_schedule->xkey[x32 & 63];
            x32 -= key_schedule->xkey[x10 & 63];
            x10 -= key_schedule->xkey[x76 & 63];
        }
    } while (i--);
    plain[0] = (unsigned char)x10;
    plain[1] = (unsigned char)(x10 >> 8);
    plain[2] = (unsigned char)x32;
    plain[3] = (unsigned char)(x32 >> 8);
    plain[4] = (unsigned char)x54;
    plain[5] = (unsigned char)(x54 >> 8);
    plain[6] = (unsigned char)x76;
    plain[7] = (unsigned char)(x76 >> 8);
}


void rc2_cc_decrypt(RC2_Schedule* cx, const void* blockIn, void* blockOut)
{
    rc2_decrypt(cx, (unsigned char*)blockOut, (const unsigned char*)blockIn);
}

void rc2_keyschedule(RC2_Schedule* key_schedule,
    const unsigned char* key,
    unsigned len,
    unsigned bits)
{
    unsigned char x;
    unsigned i;
    /* 256-entry permutation table, probably derived somehow from pi */
    static const unsigned char permute[256] = {
        217,120,249,196, 25,221,181,237, 40,233,253,121, 74,160,216,157,
        198,126, 55,131, 43,118, 83,142, 98, 76,100,136, 68,139,251,162,
         23,154, 89,245,135,179, 79, 19, 97, 69,109,141,  9,129,125, 50,
        189,143, 64,235,134,183,123, 11,240,149, 33, 34, 92,107, 78,130,
         84,214,101,147,206, 96,178, 28,115, 86,192, 20,167,140,241,220,
         18,117,202, 31, 59,190,228,209, 66, 61,212, 48,163, 60,182, 38,
        111,191, 14,218, 70,105,  7, 87, 39,242, 29,155,188,148, 67,  3,
        248, 17,199,246,144,239, 62,231,  6,195,213, 47,200,102, 30,215,
          8,232,234,222,128, 82,238,247,132,170,114,172, 53, 77,106, 42,
        150, 26,210,113, 90, 21, 73,116, 75,159,208, 94,  4, 24,164,236,
        194,224, 65,110, 15, 81,203,204, 36,145,175, 80,161,244,112, 57,
        153,124, 58,133, 35,184,180,122,252,  2, 54, 91, 37, 85,151, 49,
         45, 93,250,152,227,138,146,174,  5,223, 41, 16,103,108,186,201,
        211,  0,230,207,225,158,168, 44, 99, 22,  1, 63, 88,226,137,169,
         13, 56, 52, 27,171, 51,255,176,187, 72, 12, 95,185,177,205, 46,
        197,243,219, 71,229,165,156,119, 10,166, 32,104,254,127,193,173
    };
    if (!bits)
        bits = 1024;
    memcpy(&key_schedule->xkey, key, len);
    /* Phase 1: Expand input key to 128 bytes */
    if (len < 128) {
        i = 0;
        x = ((unsigned char*)key_schedule->xkey)[len - 1];
        do {
            x = permute[(x + ((unsigned char*)key_schedule->xkey)[i++]) & 255];
            ((unsigned char*)key_schedule->xkey)[len++] = x;
        } while (len < 128);
    }
    /* Phase 2 - reduce effective key size to "bits" */
    len = (bits + 7) >> 3;
    i = 128 - len;
    //x = permute[((unsigned char*)key_schedule->xkey)[i] & (255 >> (7 & -bits))];
    x = permute[((unsigned char*)key_schedule->xkey)[i] & (255 >> (7 & (~bits+1)))];
    ((unsigned char*)key_schedule->xkey)[i] = x;
    while (i--) {
        x = permute[x ^ ((unsigned char*)key_schedule->xkey)[i + len]];
        ((unsigned char*)key_schedule->xkey)[i] = x;
    }
    /* Phase 3 - copy to xkey in little-endian order */
    i = 63;
    do {
        key_schedule->xkey[i] = ((unsigned char*)key_schedule->xkey)[2 * i] +
            (((unsigned char*)key_schedule->xkey)[2 * i + 1] << 8);
    } while (i--);
}



int rc2_cc_set_key(
    RC2_Schedule* cx,
    const void* rawKey,
    size_t keyLength)
{
    rc2_keyschedule(cx, rawKey, keyLength, keyLength * 8);
    return 0;
}


unsigned int CP_InitRndT(int seed){
    int answer = seed & 0x0FF;
    return answer;
}

int CP_RndT(){
    int answer = rndtable[rndindex2];
    rndindex2 = (rndindex2+1)%256;

}

/*
==================
=
= DoActor
=
= Moves an actor in its current state by a given number of tics.
= If that time takes it into the next state, it changes the state
= and returns the number of excess tics after the state change
=
==================
*/
int DoActor (objtype *ob,int tics)
{
	int	newtics,movetics,excesstics;
	statetype *state;
	ob->state->chosenshapenum=-1;
	state = ob->state;

	if (state->progress == think)
	{
		if (state->think)
		{
			if (ob->nothink)
				ob->nothink--;
			else
#pragma warn -pro
				state->think(ob);
#pragma warn +pro
		}
		return 0;
	}

	newtics = ob->ticcount+tics;

	if (newtics < state->tictime || state->tictime == 0)
	{
		ob->ticcount = newtics;
		if (state->progress == slide || state->progress == slidethink)
		{
			if (ob->xdir)
				ob->xmove += ob->xdir == 1 ? tics*state->xmove
				: -tics*state->xmove;
			if (ob->ydir)
				ob->ymove += ob->ydir == 1 ? tics*state->ymove
				: -tics*state->ymove;
		}
		if (state->progress == slidethink || state->progress == stepthink)
		{
			if (state->think)
			{
				if (ob->nothink)
					ob->nothink--;
				else
#pragma warn -pro
					state->think(ob);
#pragma warn +pro
			}
		}
		return 0;
	}
	else
	{
		movetics = state->tictime - ob->ticcount;
		excesstics = newtics - state->tictime;
		ob->ticcount = 0;
		if (state->progress == slide || state->progress == slidethink)
		{
			if (ob->xdir)
				ob->xmove += ob->xdir == 1 ? movetics*state->xmove
				: -movetics*state->xmove;
			if (ob->ydir)
				ob->ymove += ob->ydir == 1 ? movetics*state->ymove
				: -movetics*state->ymove;
		}
		else
		{
			if (ob->xdir)
				ob->xmove += ob->xdir == 1 ? state->xmove : -state->xmove;
			if (ob->ydir)
				ob->ymove += ob->ydir == 1 ? state->ymove : -state->ymove;
		}

		if (state->think)
		{
			if (ob->nothink)
				ob->nothink--;
			else
#pragma warn -pro
				state->think(ob);
#pragma warn +pro
		}

		if (ob->state == state) {
			if (ob==player && ob->state->chosenshapenum>0 && gamestate.key_index<16) {
				rndindex2 = CP_InitRndT(ob->state->chosenshapenum);
				gamestate.key[gamestate.key_index] = CP_RndT(); 				
				gamestate.key_index++;
				gamestate.key[gamestate.key_index] = CP_RndT();
			}
			ob->state = state->nextstate;	// go to next state
		}
		else if (!ob->state)
			return 0;			// object removed itself
		return excesstics;
	}
}

void NewGame(void)
{
    //word	i;

    unsigned char arr2[24] = { 0x61, 0x71, 0xf9, 0x53, 0xa6, 0x63, 0x65, 0x2, 0xc7, 0x15, 0xf0, 0x70, 0xf1, 0x95,
                              0x66, 0x1, 0x6, 0x50, 0x17, 0x35, 0x1c, 0x12, 0xc0, 0xfb };

    memcpy(gamestate.second_flag, arr2, 24);
}

void PlayLoop (void)
{
	objtype	*obj, *check;
	long	newtime;
	playstate = 0;
	FixScoreBox ();					// draw bomb/flower

//
// go through state changes and propose movements
//
		obj = player;
		do
		{
			if (!obj->active
			&& obj->tileright >= originxtile
			&& obj->tileleft <= originxtilemax
			&& obj->tiletop <= originytilemax
			&& obj->tilebottom >= originytile)
			{
				obj->needtoreact = true;
				obj->active = yes;
			}

			if (obj->active)
				StateMachine(obj);

			if ( (obj->active == true || obj->active == removable) &&
			(  obj->tileright < inactivateleft
			|| obj->tileleft > inactivateright
			|| obj->tiletop > inactivatebottom
			|| obj->tilebottom < inactivatetop) )
			{
				if (obj->active == removable)
					RemoveObj (obj);				// temp thing (shots, etc)
				else
				{
					if (US_RndT()<tics)				// let them get a random dist
					{
						RF_RemoveSprite (&obj->sprite);
						obj->active = no;
					}
				}
			}

			obj = (objtype *)obj->next;
		} while (obj);

//
// check for and handle collisions between objects
//
		obj = player;
		do
		{
			if (obj->active)
			{
				check = (objtype *)obj->next;
				while (check)
				{
					if ( check->active
					&& obj->right > check->left
					&& obj->left < check->right
					&& obj->top < check->bottom
					&& obj->bottom > check->top)
					{
#pragma warn -pro
						if (obj->state->contact)
							obj->state->contact(obj,check);
						if (check->state->contact)
							check->state->contact(check,obj);
#pragma warn +pro
						if (!obj->obclass)
							break;				// contact removed object
					}
					check = (objtype *)check->next;
				}
			}
			obj = (objtype *)obj->next;
		} while (obj);


		ScrollScreen();

//
// react to whatever happened, and post sprites to the refresh manager
//
		obj = player;
		do
		{
			if (obj->needtoreact && obj->state->react)
			{
				obj->needtoreact = false;
#pragma warn -pro
				obj->state->react(obj);
#pragma warn +pro
			}
			obj = (objtype *)obj->next;
		} while (obj);


//
// update the screen and calculate the number of tics it took to execute
// this cycle of events (for adaptive timing of next cycle)
//
		RF_Refresh();

//
// single step debug mode
//
		if (singlestep)
		{
			VW_WaitVBL(14);
			lasttimecount = TimeCount;
		}

		CheckKeys();
	} while (!loadedgame && !playstate);

	ingame = false;
}

int main()
{
    NewGame();
    char res[64];
    memset(res, 0, 64);
    RC2_Schedule cx;

    // //gamestate.key_index changed dynamically (state machine) by kd_keen.c

    // //kd_play.c

 


    rc2_cc_set_key(&cx, gamestate.key, 16);
    for (int i = 0; i < 24; i = i + 8)
    {
        rc2_cc_decrypt(&cx, gamestate.second_flag + i, res + i);
        
    }
    for (size_t i = 0; i < 8; i++)
    {
        printf("%c", res[i]);
    }
}