class Solution:
    def maxOfSubarrays(self, arr, k):
        n=len(arr)
        res=[]
        cm=max(arr[:k])
        res.append(cm)
        for i in range(k,n):
            l=arr[i-k]
            r=arr[i]
            if l==cm:
                cm=max(arr[i-k+1:i+1])
            elif r>cm:
                cm=r
            res.append(cm)
        return res
