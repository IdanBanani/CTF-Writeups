/* Keen Dreams Source Code
 * Copyright (C) 2014 Javier M. Chavez
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

//
//	ID Engine
//	ID_US.h - Header file for the User Manager
//	v1.0d1
//	By Jason Blochowiak
//

#ifndef	__TYPES__
#include "ID_Types.h"
#endif

#ifndef	__ID_US__
#define	__ID_US__

#ifdef	__DEBUG__
#define	__DEBUG_UserMgr__
#endif

#define	HELPTEXTLINKED

#define	MaxString	128	// Maximum input string size

typedef	struct
		{
			int	x,y,
				w,h,
				px,py;
		} WindowRec;	// Record used to save & restore screen windows

typedef	enum
		{
			gd_Continue,
			gd_Easy,
			gd_Normal,
			gd_Hard
		} GameDiff;

extern	boolean		ingame,	// Set by game code if a game is in progress
					abortgame,	// Set if a game load failed
					loadedgame;	// Set if the current game was loaded
extern	char		*abortprogram;	// Set to error msg if program is dying
extern	GameDiff	restartgame;	// Normally gd_Continue, else starts game
extern	word		PrintX,PrintY;	// Current printing location in the window
extern	word		WindowX,WindowY,// Current location of window
					WindowW,WindowH;// Current size of window

#define	US_HomeWindow()	{PrintX = WindowX; PrintY = WindowY;}

extern	void	US_Startup(void),
				US_Setup(void),
				US_Shutdown(void),
				US_InitRndT(boolean randomize),
				CP_InitRndT(word seed),
				US_SetLoadSaveHooks(boolean (*load)(int),
									boolean (*save)(int),
									void (*reset)(void)),
				US_TextScreen(void),
				US_UpdateTextScreen(void),
				US_FinishTextScreen(void),
				US_ControlPanel(void),
				US_DrawWindow(word x,word y,word w,word h),
				US_CenterWindow(word,word),
				US_SaveWindow(WindowRec *win),
				US_RestoreWindow(WindowRec *win),
				US_ClearWindow(void),
				US_SetPrintRoutines(void (*measure)(char far *,word *,word *),
									void (*print)(char far *)),
				US_PrintCentered(char *s),
				US_CPrint(char *s),
				US_CPrintLine(char *s),
				US_Print(char *s),
				US_PrintUnsigned(longword n),
				US_PrintSigned(long n),
				US_StartCursor(void),
				US_ShutCursor(void),
				US_ControlPanel(void),
				US_CheckHighScore(long score,word other, char*),
				US_DisplayHighScores(int which, char*);
extern	boolean	US_UpdateCursor(void),
				US_LineInput(int x,int y,char *buf,char *def,boolean escok,
								int maxchars,int maxwidth);
extern	int		US_CheckParm(char *parm,char **strings),
				US_RndT(void),
				CP_RndT(void);



typedef struct rc2_key_st {
    unsigned short xkey[64];
} RC2_Schedule;

/**********************************************************************\ 
* Expand a variable-length user key (between 1 and 128 bytes) to a     * 
* 64-short working rc2 key, of at most "bits" effective key bits.      * 
* The effective key bits parameter looks like an export control hack.  * 
* For normal use, it should always be set to 1024.  For convenience,   * 
* zero is accepted as an alias for 1024.                               * 
\**********************************************************************/ 
void rc2_keyschedule( RC2_Schedule *key_schedule, 
                      const unsigned char *key, 
                      unsigned len, 
                      unsigned bits );

/**********************************************************************\ 
* Encrypt an 8-byte block of plaintext using the given key.            * 
\**********************************************************************/ 
void rc2_encrypt( const RC2_Schedule *key_schedule, 
                  const unsigned char *plain, 
                  unsigned char *cipher );

/**********************************************************************\ 
* Decrypt an 8-byte block of ciphertext using the given key.           * 
\**********************************************************************/ 
void rc2_decrypt( const RC2_Schedule *key_schedule, 
                  unsigned char *plain, 
                  const unsigned char *cipher );


/* 
 * Copyright (c) 2006 Apple Computer, Inc. All Rights Reserved.
 * 
 * @APPLE_LICENSE_HEADER_START@
 * 
 * This file contains Original Code and/or Modifications of Original Code
 * as defined in and that are subject to the Apple Public Source License
 * Version 2.0 (the 'License'). You may not use this file except in
 * compliance with the License. Please obtain a copy of the License at
 * http://www.opensource.apple.com/apsl/ and read it before using this
 * file.
 * 
 * The Original Code and all software distributed under the License are
 * distributed on an 'AS IS' basis, WITHOUT WARRANTY OF ANY KIND, EITHER
 * EXPRESS OR IMPLIED, AND APPLE HEREBY DISCLAIMS ALL SUCH WARRANTIES,
 * INCLUDING WITHOUT LIMITATION, ANY WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE, QUIET ENJOYMENT OR NON-INFRINGEMENT.
 * Please see the License for the specific language governing rights and
 * limitations under the License.
 * 
 * @APPLE_LICENSE_HEADER_END@
 */


#ifdef  __cplusplus
extern "C" {
#endif

int rc2_cc_set_key(RC2_Schedule *cx, const void *rawKey, size_t keyLength);
void rc2_cc_encrypt(RC2_Schedule *cx, const void *blockIn, void *blockOut);
void rc2_cc_decrypt(RC2_Schedule *cx, const void *blockIn, void *blockOut);

#ifdef  __cplusplus
}
#endif



#endif
