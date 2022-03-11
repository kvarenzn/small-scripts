(async (P, fs) => {
    const browser = await P.launch({headless: true});
    const page = await browser.newPage();
    await page.goto('https://comic-walker.com/contents/detail/KDCW_AM01201866010000_68/', {
        waitUntil: 'domcontentloaded'
    });

    // page loaded
    const chapterList = await page.$$('ul#reversible > li');

    for (let chapter of chapterList) {
        let title = await chapter.$eval('span', node => node.innerText);
        if (!title.match(/第\d+話.*/)) {
            // filter notification
            continue;
        }
        let [_, number, subNumber] = title.match(/第(\d+)話(.*)/);
        number = +number;
        subNumber = subNumber ? null : (subNumber.charCodeAt() - 9311);
        if (number < 3) {
            // ignore chapters before chapter 3
            continue;
        }

        let link = await chapter.$eval('a', node => node.href);

        const comicPage = await browser.newPage();
        await comicPage.goto(link, {
            waitUntil: 'domcontentloaded'
        });

        await comicPage.waitForFunction("document.querySelector('main > div > div').children.length >= 3");

        console.log(title);
        while (true) {
            await comicPage.waitForTimeout(500);
            let container = await comicPage.$('main > div > div');
            let comicPagesList = await container.$$('div.react-swipe-container > div > div');
            let currentPage;
            for (let comic of comicPagesList) {
                let transform = await comic.evaluate(node => node.style.transform);
                if (transform == 'translate(0px, 0px) translateZ(0px)') {
                    currentPage = comic;
                    break;
                }
            }
            if (!currentPage) {
                break;
            }
            let cvs = await currentPage.$('canvas');
            if (!cvs) {
                break;
            }
            let data = await cvs.evaluate(cvs => cvs.toDataURL());
            let chapter = '' + number;
            if (!fs.existsSync(chapter)) {
                fs.mkdirSync(chapter);
            }

            let files = fs.readdirSync(chapter);
            let currentNumber = '' + (files.length + 1);
            currentNumber = currentNumber.length > 1 ? currentNumber : '0' + currentNumber;
            fs.writeFileSync(`${chapter}/${currentNumber}.png`, Buffer.from(data.split(',')[1], 'base64'));
            console.log(currentNumber);

            if (await currentPage.$('div')) {
                break;
            }
            await comicPage.keyboard.press('ArrowLeft');
        }
        await comicPage.close();
    }

    await browser.close();
})(require('puppeteer'), require('fs'));