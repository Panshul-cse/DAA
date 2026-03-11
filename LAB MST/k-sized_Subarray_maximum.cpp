class Solution {
  public:
    vector<int> maxOfSubarrays(vector<int>& arr, int k) {
        int n = arr.size();
        vector<int> ans_arr;
        if (n == 0 || k == 0) return ans_arr;

        for (int i = 0; i <= n - k; i++) {
            int cr_max = arr[i];  
            for (int j = i; j < i + k; j++) {
                cr_max = max(cr_max, arr[j]);
            }
            ans_arr.push_back(cr_max);
        }
        return ans_arr;
    }
};
