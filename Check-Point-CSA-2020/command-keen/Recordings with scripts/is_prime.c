int is_prime(int num) {
    int i, lim = (int) sqrt(num);
    if (num == 2)
        return 1;
    if (num < 2 || num % 2 == 0)
        return 0;
    for (i = 3; i <= lim; i += 2)
        if (num % i == 0)
            return 0;
    return 1;
}