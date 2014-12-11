# When giving gifts, consumers usually keep in mind two variables - cost and quantity. In order to facilitate better gift-giving on the Zappos
# website, the Software Engineering team would like to test a simple application that allows a user to submit two inputs: N (desired # of products) and X
# (desired dollar amount). The application should take both inputs and leverage the Zappos API (http://developer.zappos.com/docs/api-documentation) to create a list
# of Zappos products whose combined values match as closely as possible to X dollars. For example, if a user entered 3 (# of products) and $150, the
# application would print combinations of 3 product items whose total value is closest to $150.



# This procedure is written by Python 2.7.

#     import urllib
#     url = 'http://api.zappos.com/Search?includes=[%22facets%22]&facets=[%22productTypeFacet%22,%22price%22]&key=52ddafbe3ee659bad97fcce7c53592916a6bfd73'
#     response = urllib.urlopen(url)
#     content = response.read()
#     print content


ProductMap = [{"productName":"prod1","price":"$94.00"}, {"productName":"prod2","price":"$37.00"}, {"productName":"prod3","price":"$45.00"}, {"productName":"prod4","price":"$103.00"}, {"productName":"prod5","price":"$102.00"}, {"productName":"prod6","price":"$55.00"}, {"productName":"prod7","price":"$37.00"}, {"productName":"prod8","price":"$94.00"}, {"productName":"prod9","price":"$100.00"}, {"productName":"prod10","price":"$33.00"}, {"productName":"prod11","price":"$31.00"}]

# Convert ProductMap to a new data structure. In the array, there are tuples. The first element in the tuple is productName and the second is the corresponding price value.
# T(n) = O(n)
def GetProdPriceFromMap(p):
    ProductInfo = []
    for i in p:
        price = float(i["price"][1:])
        product = i["productName"]
        combo = [product, price]
        ProductInfo.append(combo)
    return ProductInfo

# Sort the Array on price
# T(n) = O(nlogn)
def getKey(k):
    return k[1]

def SortProdOnPrice(p):
    array = GetProdPriceFromMap(p)
    return sorted(array, key = getKey)

# Main Procedure to get all the product combo (count < 2)
# T(n) = O(n)
def Find1ProdInArray(numarray, begin, count, target):
    allprodcombo = []
    minval = float("inf")
    if count <= 0:
        return "Please input the number of products you want."
    
    elif count == 1:
        for i in range(begin, len(numarray)):
            if numarray[i][1] == target:
                if minval != 0:
                    minval = 0
                    allprodcombo = []
                    allprodcombo.append(numarray[i][0])
                else:
                    allprodcombo.append(numarray[i][0])
            
            elif numarray[i][1] < target:
                if target - numarray[i][1] < minval:
                    allprodcombo = []
                    minval = target - numarray[i][1]
                    allprodcombo.append(numarray[i][0])
                    
                elif target - numarray[i][1] == minval:
                    allprodcombo.append(numarray[i][0])
                    
            else:
                if numarray[i][1] - target < minval:
                    allprodcombo = []
                    minval = numarray[i][1] - target
                    allprodcombo.append(numarray[i][0])
                    
                elif numarray[i][1] - target == minval:
                    allprodcombo.append(numarray[i][0])
                    
        return allprodcombo
            
# Main Procedure to get all the product combo (count >= 2)
# T(n) = O(nlogn) if count == 2
# T(n) = O(n^(k-1)) if count == k > 2
def FindKProdInSortedArray(numarray, begin, count, target):
    allprodcombo = []
    comboprod = []
    minval = float("inf")
    if count == 2:
        i = begin
        j = len(numarray) - 1
        while i < j:
            sum = numarray[i][1] + numarray[j][1]
            if sum == target:
                if minval != 0:
                    minval = 0
                    allprodcombo = []
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                else:
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                i += 1
                j -= 1
            
            elif sum < target:
                if target - sum < minval:
                    minval = target - sum
                    allprodcombo = []
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                    
                elif target - sum == minval:
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                i += 1
            
            else:
                if sum - target < minval:
                    minval = sum - target
                    allprodcombo = []
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                
                elif sum - target == minval:
                    comboprod = []
                    comboprod.append(numarray[i][0])
                    comboprod.append(numarray[j][0])
                    allprodcombo.append(comboprod)
                j -= 1
    
    else:
        for k in range(begin, len(numarray)):
            suballprodcombo = FindKProdInSortedArray(numarray, k + 1, count - 1, target - numarray[k][1])
            if suballprodcombo:
                for j in range(0,len(suballprodcombo)):
                    suballprodcombo[j].insert(0, numarray[k][0])
                for i in range(0,len(suballprodcombo)):
                    allprodcombo.append(suballprodcombo[i])
                    
    return allprodcombo

# Public function to achieve the results
# T(n) = O(1), if count < 1
# T(n) = O(n), if count = 1
# T(n) = O(nlogn), if count = 2
# T(n) = O(n^(k-1)), if count = k > 2
def OfferCustomersDesiredProdCombos(count, target):
    begin = 0
    if count < 2:
        numarray = GetProdPriceFromMap(ProductMap)
        return Find1ProdInArray(numarray, begin, count, target)
    else:
        numarray = SortProdOnPrice(ProductMap)
        return FindKProdInSortedArray(numarray, begin, count, target)


print OfferCustomersDesiredProdCombos(5, 131)

