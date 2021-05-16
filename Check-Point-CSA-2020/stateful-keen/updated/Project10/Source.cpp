#include <iostream>

uint16_t rndindex;
uint16_t rndindex2;

static const unsigned char randtable[] = {
	0,   8, 109, 220, 222, 241, 149, 107,  75, 248, 254, 140,  16,  66,
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
	 120, 163, 236, 249
};

void CP_InitRndT(uint16_t seed) {
	uint16_t ax = seed;
	ax &= 0xff;
	rndindex2 = ax;
}
int CP_RndT(void)
{
	uint16_t bx = rndindex2;
	int rand = randtable[bx++];
	bx &= 0xff;
	rndindex2 = bx;
	return rand;
}

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
#pragma warning (disable : 4146)
	x = permute[((unsigned char*)key_schedule->xkey)[i] & (255 >> (7 & -bits))];
#pragma warning (enable : 4146)
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

/**********************************************************************\
* Decrypt an 8-byte block of ciphertext using the given key.           *
\**********************************************************************/
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
	do {
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
		if (i == 5 || i == 11) {
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

int rc2_cc_set_key(
	RC2_Schedule* cx,
	const unsigned char* rawKey,
	size_t keyLength)
{
	rc2_keyschedule(cx, rawKey, keyLength, keyLength * 8);
	return 0;
}

void rc2_cc_decrypt(RC2_Schedule* cx, const void* blockIn, void* blockOut)
{
	rc2_decrypt(cx, (unsigned char*)blockOut, (const unsigned char*)blockIn);
}

int main()
{
	int chosenshapenum = 1;
	int key_index = 0;
	unsigned char key[16]{ 0 };
	unsigned char second_flag[24] = { 0x61, 0x71, 0xf9, 0x53, 0xa6, 0x63, 0x65, 0x2, 0xc7, 0x15, 0xf0, 0x70, 0xf1, 0x95,
	0x66, 0x1, 0x6, 0x50, 0x17, 0x35, 0x1c, 0x12, 0xc0, 0xfb };
	char res[64];
	RC2_Schedule cx;

	key_index = 0;

	//levels : 0 ,2 ,4 , 6 ,8 ,10 ,12 ,14
	int indexes[8] = { 93, 100, 137 , 137 , 73, 74 , 75 , 76 };

	for (size_t i = 0; i < sizeof(indexes)/sizeof(int); i++)
		{
		CP_InitRndT((uint16_t)indexes[i]);
		key[key_index] = CP_RndT();
		key_index++;
		key[key_index] = CP_RndT();
		key_index++;
		}
	
	memset(res, 0, 64);

	rc2_cc_set_key(&cx, key, 16);

	for (int i = 0; i < 24; i = i + 8) {
		rc2_cc_decrypt(&cx, second_flag + i, res + i);
	}

	std::cout << res << std::endl;


}
