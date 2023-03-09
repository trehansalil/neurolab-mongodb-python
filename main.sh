# shellcheck disable=SC2164
echo "$1" 'is the organisationId for which the data is getting downloaded'



curl 'https://data.gsmaintelligence.com/api-web/v2/xls-report?reportType=Fixed-by-operator&dataType=fixed-operator&organisationType==fixed-operator&dateFrom=2022-01-01&dateTo=2024-10-01&dateType=Q&organisationOwnership.organisationId='"$1"'&currencyId==2&isSpotPrice==true&reportName=Fixed-by-operator' \
  -H 'authority: data.gsmaintelligence.com' \
  -H 'accept: */*' \
  -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'cache-control: no-cache' \
  -H 'content-type: text/plain' \
  -H 'cookie:'"$2"' ' \
  -H 'dnt: 1' \
  -H 'pragma: no-cache' \
  -H 'referer: https://data.gsmaintelligence.com/data/fixed-operator-metrics' \
  -H 'sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' \
  --compressed  \
  --output "$3"/data_"$3"_"$4".xlsx

# curl 'https://www.themoviedb.org/search/trending?query=Predestinado%3A%20Arig%C3%B3%20e%20o%20Esp%C3%ADrito%20do%20Dr.%20Fritz' \
#   -H 'authority: www.themoviedb.org' \
#   -H 'accept: */*' \
#   -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
#   -H 'cookie: tmdb.prefs=%7B%22adult%22%3Afalse%2C%22i18n_fallback_language%22%3A%22en-US%22%2C%22locale%22%3A%22en-GB%22%2C%22country_code%22%3A%22IN%22%2C%22timezone%22%3A%22Asia%2FKolkata%22%7D; _ga=GA1.2.1756090481.1650536483; _gid=GA1.2.1425136332.1650536483; _dc_gtm_UA-2087971-10=1; tmdb.session=Aebxdx7ngKBMhNcTiXzLX7Tfx8tTz8kgow3san0ZXmiZbtkbl9ZqZNwwT4vkqtJEV9wQW3zJUcSqi3mfPG3cZsaF1avlyajki4B6OugvvOG_sdm4yI7yyzp6DGoji8uVgC1_x5fklfRow8o2uqZN0dLqZ1nIcwnDFi-onwfg_ZgQu6m9Gi3xNC0xPHsV0S0VpIoYju94LLsWBuy7ZTq25eqC8QrcWLktTRuHqywSEagw; _gali=search_v4' \
#   -H 'dnt: 1' \
#   -H 'referer: https://www.themoviedb.org/movie/649985-predestinado' \
#   -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36' \
#   -H 'x-requested-with: XMLHttpRequest' \
#   --compressed

# curl 'https://data.gsmaintelligence.com/api-web/v2/xls-report?reportType=Mobile-by-operator&dataType=operator&organisationType==operator&dateFrom=2018-01-01&dateTo=2022-01-01&dateType=Q&organisationOwnership.organisationId='"$1"'&currencyId==-1&isSpotPrice==false&reportName=Mobile-by-operator' \
#   -H 'authority: data.gsmaintelligence.com' \
#   -H 'accept: */*' \
#   -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
#   -H 'content-type: text/plain' \
#   -H 'cookie:'"$2"' ' \
#   -H 'dnt: 1' \
#   -H 'referer: https://data.gsmaintelligence.com/data/operator-metrics' \
#   -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Windows"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36' \
#   --compressed \
#   --output data "$1".xlsx