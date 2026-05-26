Open your desktop browser and log into X.

Go straight to your following tab: https://x.com/your_username/following

Keep hitting the Page Down key or scroll down until the list stops loading (so all 176 accounts are fully loaded on your screen).

Right-click anywhere on the page, select Inspect (or press F12), and switch to the Console tab.

Paste the following snippet into the console and hit Enter:

'''
(async () => {
    console.log("开始自动滚动并收集关注列表，请勿关闭页面...");
    
    let allUsers = new Set();
    let lastCount = 0;
    let checkCount = 0;
    
    // 持续滚动，直到没有新内容加载出来为止
    while (checkCount < 10) {
        // 抓取当前页面上所有可见的账号节点
        document.querySelectorAll('[data-testid="UserCell"]').forEach(el => {
            let textBlocks = el.innerText.split('\n');
            if (textBlocks.length >= 2) {
                let displayName = textBlocks[0];
                let username = textBlocks[1].startsWith('@') ? textBlocks[1] : textBlocks[2];
                
                if (username && username.startsWith('@')) {
                    allUsers.add(`${displayName} (${username})`);
                }
            }
        });
        
        // 打印当前进度
        if (allUsers.size !== lastCount) {
            console.log(`已收集 ${allUsers.size} 个账号...`);
            lastCount = allUsers.size;
            checkCount = 0;
        } else {
            // 如果数量没变，可能还在加载，多等几次
            checkCount++;
        }
        
        // 向下滚动一段距离
        window.scrollBy(0, window.innerHeight * 0.8);
        // 等待网络请求和 DOM 渲染（700ms 比较稳妥）
        await new Promise(resolve => setTimeout(resolve, 700));
    }
    
    console.log(`\n完成！共抓取到 ${allUsers.size} 个关注账号。列表如下：\n`);
    console.log(Array.from(allUsers).join('\n'));
})();
'''
