### Inprogress
* https://www.youtube.com/watch?v=AuBai920D0E 보고 infinit scroll넣기

### Next
* static에서 작물 클릭하면 최근 5일간 거래량 그래프로 보여주기
* 표준 품목코드 조회 화면 추가


### Finished
* 날짜 선택 기능
* crawl결과 query
* 달력 만들기
  >auction_list page에 날짜가 한개 밖에 안보임
  >bootstrap의 datepicker로 해서 날짜를 넘길 수 있게
* auction_result 페이징 구현
  > 마지막 결과를 저장하고 있다가
* crawl result에 Next붙이기
* 거래된것만 가지고 오는 query만들기
  > FilterExpression: 'Sales >= :platinum'
* update function추가 
* 품목명 추가
* crawl_result에 오늘 날짜 0개면 데이터 있는 날짜를 보여주기
* 해당 날짜에 데이터가 없으면 있는날짜 데이터 보여주기
* crawl_result total_cnt기준으로 내림차순 정렬해서 보여주기
> sort에 문제가 있을 수 있다.
* 누르면 해당 작물 데이터 화면으로 이동 '작물 상세'
* 평균 거래 가격도 추가(작물마다 단위가 다른 문제가 있음)
> 작물별로 단위 확인하는 기능(단, 상자, 봉지, 기타 등)
> 각 작물의 단위별로 group by하는 기능 필요한 것 같음
> select all기능 왜냐하면 한번에 1mb밖에 쿼리를 못하기 때문

