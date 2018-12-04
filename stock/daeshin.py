import win32com.client
from datetime import datetime

class Daeshin():
    def login(self):
        """
        서버가 정상적으로 연결되었는지 확인하는 함수
        Args:

        Returns:
            1: 연결 정상, 2: 연결 비정상

        Example:
            isConnected = login()
        """
        instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        return instCpCybos.IsConnect

    def get_market_list(self):
        """
        사용가능한 마켓 정보 리스트를 리턴하는 함수
        Args:

        Returns:
            {0: "구분없음", 1: "거래소", 2: "코스닥", 3: "프리보드", 4: "KRX"}

        Example:
            market_list = market_list()
        """
        market_list = {0: "구분없음", 1: "거래소", 2: "코스닥", 3: "프리보드", 4: "KRX"}
        return market_list

    def subMarketEye(self, m_InfoList, m_Code):
        """
        get_item_dict함수를 위한 api사용 함수
        Args:
            m_InfoList : 원하는 정보 인덱스 값
            m_Code : 종목코드

        Returns:
            {"종목코드": "A005930", "PER": 1, ....}

        Example:
            subMarketEye([1,2,3],"A005930")
        """
        # ## 대신 api 세팅
        obj = win32com.client.Dispatch("cpsysdib.MarketEye")
        obj.SetInputValue(0, m_InfoList)     # A:시장전체 선택
        obj.SetInputValue(1, m_Code)      # 종목
        obj.BlockRequest()

        numField=obj.GetHeaderValue(0)        # 필드수
        numData=obj.GetHeaderValue(2)         # 데이터수(종목수)
        # nameField=obj.GetHeaderValue(1)
        # print('필드명:', nameField)
        data=[]
        for ixRow in range(numData):
            tempdata=[]
            for ixCol in range(numField):
                tempdata.append(obj.GetDataValue(ixCol, ixRow))
            data.append(tempdata)
        return data[0]

    def get_item_list(self, market):
        """
        해당 마켓에 해당하는 종목코드,종목명을 리턴해주는 함수
        Args:
            market : 조회를 원하는 마켓이름(get_market_list() 함수를 통해 알수 있다)

        Returns:
            {'A000020': '동화약품', 'A000030': '우리은행'...}

        Example:
            get_item_list("거래소")
        """
        market_dict = self.get_market_list()
        marketCode = ''
        for marketC, marketN in market_dict.items():
            if marketN == market:
                marketCode = marketC

        instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        codeList = instCpCodeMgr.GetStockListByMarket(marketCode)
        stock = {}
        for code in codeList:
            name = instCpCodeMgr.CodeToName(code)
            stock[code] = name
        return stock
    def get_item_dict(self, code):
        """
        종목코드에 해당하는 해당 종목 재무정보를 리턴해주는 함수
        Args:
            code : 종목코드

        Returns:
            {"종목코드": "A005930", "PER": 1, ....}

        Example:
            get_item_dict("A005930")
        """
        m_InfoList = [0, 67, 70, 71, 74, 75, 76, 77, 78, 79, 80, 82, 86, 87, 88, 89, 90, 91, 92, 93, 95, 96, 98, 99,
                      100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 111]
        m_Info_desc_List = ['종목코드', 'PER', 'EPS', '자본금', '배당수익률', '부채비율', '유보율', '자기자본이익률', '매출액증가율', '경상이익증가율',
                                      '순이익증가율', 'VR', '매출액', '경상이익', '당기순이익', 'BPS', '영업이익증가율', '영업이익', '매출액영업이익률',
                                      '매출액경상이익률', '결산년월', '분기BPS', '분기영업이익증가율', '분기경상이익증가율', '분기순이익증가율', '분기매출액', '분기영업이익',
                                      '분기경상이익', '분기당기순이익', '분기매출액영업이익률', '분기매출액경상이익률', '분기ROE', '분기유보율', '분기부채비율', '최근분기년월']

        ### 자료가져오기
        data = self.subMarketEye(m_InfoList, code)

        return dict(zip(m_Info_desc_List, data))



    def get_price_type(self, price_type):
        """
        가격 타입을 입력하면 대신증권api에서 사용하는 인덱스값으로 변환해주는 함수
        """
        if price_type == "일":
            return "D"
        if price_type == "주":
            return "W"
        if price_type == "월":
            return "M"
        if price_type == "분":
            return "m"
        if price_type == "틱":
            return "T"

    def get_price_list(self, code, price_type="일",fieldType = ["날짜","시간","시가","고가","저가","종가"], range_dict={'start': datetime.today(), 'end': datetime.today()}):
        """
        종목코드, 가격타입, 기간을 입력하면 해당 기간의 가격정보를 리턴해주는 함수
        Args:
            code : 종목코드
            price_type : 가격타입
            fieldType : 조회 원하는 값 리스트
            range_dict : 조회를 원하는 기간

        Returns:
            [{'날짜': 20181105, '시가': 43750, '고가': 43800, '저가': 42900, '종가': 43800, '거래량': 9426777}, {'날짜': 20181102,...]

        Example:
            get_price_list("A005930")
        """

        def trans_text2index_StockChart(StockCharInputList):
            stockChartInputTypeList = ["날짜", "시간", "시가", "고가", "저가", "종가", "전일대비", "거래량", "거래대금",
                                       "누적체결매도수량", "상장주식수", "시가총액", "외국인주문한도수량", "외국인주문가능수량",
                                       "외국인현보유수량", "수정주가일자", "수정주가비율", "기관순매수", "기관누적순매수",
                                       "등락주선", "등락비율", "예탁금", "주식회전율", "거래성립률", "대비부호"]
            indexList = []

            for i in StockCharInputList:
                indexList.append(stockChartInputTypeList.index(i))

            return tuple(indexList)
        print(fieldType)
        price_type = self.get_price_type(price_type)
        # Create object
        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        # SetInputValue
        instStockChart.SetInputValue(0, code)
        instStockChart.SetInputValue(1, ord('1'))
        instStockChart.SetInputValue(2, range_dict["end"].strftime('%Y%m%d'))
        instStockChart.SetInputValue(3, range_dict["start"].strftime('%Y%m%d'))
        instStockChart.SetInputValue(5, trans_text2index_StockChart(fieldType))
        instStockChart.SetInputValue(6, ord(price_type))
        instStockChart.SetInputValue(9, ord('1'))

        # BlockRequest
        instStockChart.BlockRequest()

        # GetHeaderValue
        numData = instStockChart.GetHeaderValue(3)
        numField = instStockChart.GetHeaderValue(1)


        resultDate = []

        # GetDataValue

        for i in range(numData):
            tmp = []
            for j in range(numField):
                print(instStockChart.GetDataValue(j, i))
                tmp.append((instStockChart.GetDataValue(j, i)))
            resultDate.append(dict(zip(fieldType, tmp)))

        return resultDate


    def get_cur_price(self, code):
        """
        종목코드, 가격타입, 기간을 입력하면 해당 기간의 가격정보를 리턴해주는 함수
        Args:
            code : 종목코드
            price_type : 가격타입
            fieldType : 조회 원하는 값 리스트
            range_dict : 조회를 원하는 기간

        Returns:
            [{'날짜': 20181105, '시가': 43750, '고가': 43800, '저가': 42900, '종가': 43800, '거래량': 9426777}, {'날짜': 20181102,...]

        Example:
            get_price_list("A005930")
        """

        # Create object
        instStockChart = win32com.client.Dispatch("dscbo1.StockMst")

        # SetInputValue
        instStockChart.SetInputValue(0, code)

        # BlockRequest
        instStockChart.BlockRequest()
        # GetHeaderValue
        numData = instStockChart.GetHeaderValue(0)
        numField = instStockChart.GetHeaderValue(1)


        resultDate = []

        print(numData)
        print(numField)

        return resultDate

#a = Daeshin()
#a.get_cur_price("A005930")
#print(a.get_price_list("A005930", "일",["날짜","종가"],{'start': datetime(2018,11,1), 'end': datetime(2018,11,5)}))
import sys
from PyQt5.QtWidgets import *
import win32com.client


class CpEvent:
    def set_params(self, client):
        self.client = client

    def OnReceived(self):
        code = self.client.GetHeaderValue(0)  # 종목코도
        name = self.client.GetHeaderValue(1)  # 종목명
        timess = self.client.GetHeaderValue(18)  # 초
        exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
        cprice = self.client.GetHeaderValue(13)  # 현재가
        diff = self.client.GetHeaderValue(2)  # 대비
        cVol = self.client.GetHeaderValue(17)  # 순간체결수량
        vol = self.client.GetHeaderValue(9)  # 거래량

        if (exFlag == ord('1')):  # 동시호가 시간 (예상체결)
            print("실시간(예상체결)", name, timess, "*", cprice, "대비", diff, "체결량", cVol, "거래량", vol)
        elif (exFlag == ord('2')):  # 장중(체결)
            print("실시간(장중 체결)", name, timess, cprice, "대비", diff, "체결량", cVol, "거래량", vol)


class CpStockCur:
    def Subscribe(self, code):
        self.objStockCur = win32com.client.Dispatch("DsCbo1.StockCur")
        handler = win32com.client.WithEvents(self.objStockCur, CpEvent)
        self.objStockCur.SetInputValue(0, code)
        handler.set_params(self.objStockCur)
        self.objStockCur.Subscribe()

    def Unsubscribe(self):
        self.objStockCur.Unsubscribe()

class GetCurStockPrice():
    def __init__(self):
        self.isSB = False
        self.objStockCur1 = CpStockCur()
        self.GetCurStockPriceSub()
        self.GetCurStockPriceUnSub()

    def GetCurStockPriceUnSub(self):
        if self.isSB:
            self.objStockCur1.Unsubscribe()
        self.isSB = False

    def GetCurStockPriceSub(self, subStockCode = "A003540"):

        self.objStockCur1.Subscribe(subStockCode)  # 대신증권

        print("실시간 현재가 요청 시작")
        self.isSB = True

a = GetCurStockPrice()
a.GetCurStockPriceSub()
