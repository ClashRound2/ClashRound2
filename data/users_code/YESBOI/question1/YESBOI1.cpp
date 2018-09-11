#include<iostream>

int main()
{
	int x,n;

	std::cin >> n;

	for(int i = 0; i < n; ++i)
	{
		std::cin >> x;

		if(x == 1)
			std::cout << x << '\n';

		else
			std::cout << x * 2 << '\n';
	}

return 0;
}