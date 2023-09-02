# Portfolio

**Разработать программу на основе алгоритма распределения ключей Диффи-Хэлмана**

**Задания для выполнения**
1. Реализация алгоритма Диффи-Хэлмана в виде клиент-серверного приложения
2. Создание зашифрованной передачи данных и команд между двумя устройствами;

**Протокол Диффи-Хэлмана**

Обмен ключами Деффи-Хэлмана (DH) — криптографический алгоритм, ко-торый позволяет интернет-протоколам согласовывать общий ключ и устанавливать безопасное соединение. Он является основой для таких протоколов, как Hypertext Transport Protocol Secure (HTTPS), Secure Shell (SSH), Internet Protocol Security (IPsec), Simple Mail Transfer Protocol Secure (SMTPS) и других протоколов, которые полагаются на Transport Layer Security (TLS). Многие протоколы используют алгоритм Деффи-Хэлмана для достижения идеальной прямой секретности (perfect forward secrecy) — функции, при которой компрометация долгосрочных ключей, используемых для аутентификации, не компрометирует сеансовые ключи для прошлых подключений. 
Весь проект разработан на объектно-ориентированном языке программирования Python. Данный проект состоит из архива файлов:
1. Файл Dist - находятся скомпилированные файлы для запуска на Linux и на Windows.
2. Файл Client - с предвычисленными константами, основной алгоритм и код.
3. Файл DHE - Ядро с длинной арифметикой: библиотека функций, реали-зующих на Python достаточно быстрое умножение по модулю и возведение в сте-пень по модулю очень больших натуральных чисел.
4. Файл design — код графического пользовательского интерфейса, кото-рый разработан в Qt Designer.

**Как работает алгоритм:**

Алгоритм может быть использован для распределения ключей, между пользователями А и Б и для создания общего секретного ключа. Совместно с удалённой стороной устанавливает открытые значении P (публичный ключ) и G для общей односторонней функции, где Р является простым числом. Эта информация не является секретной. Первый абонент А и второй абонент Б выбирают случайные числа и хранят его в секрете. А подставляет число XA в общую функцию и вычисляет результат функции остатка от деления mod и обозначает результат своего вычисления как YA. Второй пользователь Б подставляет число XБ вычисляет ту же функцию остатка от деления и обозначает результат своего вычисления как YБ. Y должно являться первообразным корнем по модулю P. Далее происходит обмен результатами между пользователями и вычисляется общий ключ Z. Общий ключ является одинаковым для собеседников, но при этом его не может получить преступник, так как данный ключ не передается между абонентами.

![image](https://github.com/uldanaadl/Portfolio/assets/143841833/c53d2897-b0e5-430a-8e4e-989540dc4312)
