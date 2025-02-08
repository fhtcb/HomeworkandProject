// 解析参数
const params = new URL(location.href).searchParams;
const _tabId = parseInt(params.get("tabId"));
window.isPopup = _tabId ? true : false;

// 当前页面
const $mediaList = $('#mediaList');
const $current = $("<div></div>");
const $currentCount = $("#currentTab #quantity");
let currentCount = 0;
// 其他页面
const $allMediaList = $('#allMediaList');
const $all = $("<div></div>");
const $allCount = $("#allTab #quantity");
let allCount = 0;
// 疑似密钥
const $maybeKey = $("<div></div>");
// 提示 操作按钮 DOM
const $tips = $("#Tips");
const $down = $("#down");
const $mergeDown = $("#mergeDown");
// 储存所有资源数据
const allData = new Map([
    [true, new Map()],  // 当前页面
    [false, new Map()]  // 其他页面
]);
// 筛选
const $filter_ext = $("#filter #ext");
// 储存所有扩展名，保存是否筛选状态 来判断新加入的资源 立刻判断是否需要隐藏
const filterExt = new Map();
// 当前所在页面
let activeTab = true;
// 储存下载id
const downData = [];
// 图标地址
const favicon = new Map();
// 当前页面DOM
let pageDOM = undefined;
// HeartBeat
chrome.runtime.sendMessage(chrome.runtime.id, { Message: "HeartBeat" });
// 清理冗余数据
chrome.runtime.sendMessage(chrome.runtime.id, { Message: "clearRedundant" });
// 复选框状态 点击返回或者全选后 影响新加入的资源 复选框勾选状态
let checkboxState = true;

// 生成资源DOM
function AddMedia(data, currentTab = true) {
    data._title = data.title;
    data.title = stringModify(data.title);
    // 不存在扩展使用类型
    if (data.ext === undefined && data.type !== undefined) {
        data.ext = data.type.split("/")[1];
    }
    // 正则匹配的备注扩展
    if (data.extraExt) {
        data.ext = data.extraExt;
    }
    //文件名
    data.name = isEmpty(data.name) ? data.title + '.' + data.ext : decodeURIComponent(stringModify(data.name));
    //截取文件名长度
    let trimName = data.name;
    if (data.name.length >= 50 && !isPopup) {
        trimName = trimName.substr(0, 20) + '...' + trimName.substr(-30);
    }
    //添加下载文件名
    Object.defineProperty(data, "pageDOM", {
        get() { return pageDOM; }
    });
    data.downFileName = G.TitleName ? templates(G.downFileName, data) : data.name;
    // 文件大小单位转换
    data._size = data.size;
    if (data.size) {
        data.size = byteToSize(data.size);
    }
    // 是否需要解析
    data.parsing = false;
    if (isM3U8(data)) {
        data.parsing = "m3u8";
    } else if (isMPD(data)) {
        data.parsing = "mpd";
    } else if (isJSON(data)) {
        data.parsing = "json";
    }
    // 网站图标
    if (data.favIconUrl && !favicon.has(data.webUrl)) {
        favicon.set(data.webUrl, data.favIconUrl);
    }
    data.isPlay = isPlay(data);

    if (allData.get(currentTab).has(data.requestId)) {
        data.requestId = data.requestId + "_" + Date.now().toString();
    }

    //添加html
    data.html = $(`
        <div class="panel">
            <div class="panel-heading">
                <input type="checkbox" class="DownCheck"/>
                ${G.ShowWebIco ? `<img class="favicon ${!data.favIconUrl ? "faviconFlag" : ""}" requestId="${data.requestId}" src="${data.favIconUrl}"/>` : ""}
                <img src="img/regex.png" class="favicon regex ${data.isRegex ? "" : "hide"}" title="${i18n.regexTitle}"/>
                <span class="name ${data.parsing || data.isRegex || data.tabId == -1 ? "bold" : ""}">${trimName}</span>
                <span class="size ${data.size ? "" : "hide"}">${data.size}</span>
            </div>
            <div class="url hide">
                <div id="mediaInfo" data-state="false">
                    ${data.title ? `<b>标题:</b> ${data.title}` : ""}
                    ${data.type ? `<br><b>MIME:</b>  ${data.type}` : ""}
                <a href="${data.url}" target="_blank" download="${data.downFileName}">${data.url}</a>
            <div>
                <button id="start-monitor">开始监测</button>
                <button id="stop-monitor">停止监测</button>
            </div>
            <ul id="messages">websocket messages
            </ul>
        </div>`);
    ////////////////////////绑定事件////////////////////////
    //展开网址
    data.urlPanel = data.html.find(".url");
    data.urlPanelShow = false;
    data.panelHeading = data.html.find(".panel-heading");
    data.panelHeading.click(function (event) {
        data.urlPanelShow = !data.urlPanelShow;
        const mediaInfo = data.html.find("#mediaInfo");
        const preview = data.html.find("#preview");
        if (!data.urlPanelShow) {
            if (event.target.id == "play") {
                preview.show().trigger("play");
                return false;
            }
            data.urlPanel.hide();
            !preview[0].paused && preview.trigger("pause");
            return false;
        }
        data.urlPanel.show();
        if (!mediaInfo.data("state")) {
            mediaInfo.data("state", true);
            if (isM3U8(data)) {
                const hls = new Hls({ enableWorker: false });
                setRequestHeaders(data.requestHeaders, function () {
                    hls.loadSource(data.url);
                    hls.attachMedia(preview[0]);
                });
                hls.on(Hls.Events.BUFFER_CREATED, function (event, data) {
                    if (data.tracks && !data.tracks.audiovideo) {
                        !data.tracks.audio && mediaInfo.append(`<br><b>${i18n.noAudio}</b>`);
                        !data.tracks.video && mediaInfo.append(`<br><b>${i18n.noVideo}</b>`);
                    }
                });
                hls.on(Hls.Events.ERROR, function (event, data) {
                    if (data.error.message == "Unsupported HEVC in M2TS found") {
                        hls.stopLoad();
                        mediaInfo.append(`<br><b>${i18n.hevcPreviewTip}</b>`);
                    }
                });
                hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
                    if (data.levels.length > 1 && !mediaInfo.text().includes(i18n.m3u8Playlist)) {
                        mediaInfo.append(`<br><b>${i18n.m3u8Playlist}</b>`);
                    }
                });
            } else if (data.isPlay) {
                setRequestHeaders(data.requestHeaders, function () {
                    preview.attr("src", data.url);
                });
            } else if (isPicture(data)) {
                setRequestHeaders(data.requestHeaders, function () {
                    data.html.find("#screenshots").show().attr("src", data.url);
                });
                return false;
            } else {
                return false;
            }
            preview.on("loadedmetadata", function () {
                preview.show();
                if (this.duration && this.duration != Infinity) {
                    data.duration = this.duration;
                    mediaInfo.append(`<br><b>${i18n.duration}:</b> ` + secToTime(this.duration));
                }
                if (this.videoHeight && this.videoWidth) {
                    mediaInfo.append(`<br><b>${i18n.resolution}:</b> ` + this.videoWidth + "x" + this.videoHeight);
                    data.videoWidth = this.videoWidth;
                    data.videoHeight = this.videoHeight;
                }
            });
        }
        if (event.target.id == "play") {
            preview.show().trigger("play");
        }
        return false;
    });


    // 绑定 start-monitor 按钮事件
    data.html.find("#start-monitor").click(function () {
        console.log("绑定成功：start-monitor");
        // 这里可以添加实际的监测逻辑
        const socket = new WebSocket("ws://8.137.110.236:8000/ws");

        data.socket = socket;

        socket.onopen = function () {
            console.log("socket open");
            socket.send(`start_monitor:${data.url}`);
        };
        // debug,添加到messages列表
        const messages = data.html.find("#messages");
        messages.append(`<li>start-monitor clicked</li>`);

        // websocket 接受的消息也放在 messages 列表中,注意，这里可能是存在长时间的等待，需要一直接受消息
        socket.onmessage = function (event) {
            console.log("socket onmessage: ", event.data);
            messages.append(`<li>${event.data}</li>`);
            // 检查接受的消息里面是否含有"https://mlearning.sjtu.edu.cn",如果有，就访问对应的url
            // 内容大概是这样的
            // 在视频流 http://8.137.110.236:8080/live/livestream.flv 中检测到二维码。 数据: https://mlearning.sjtu.edu.cn/lms/mobile/forscan/?courseCode=70185&rollCallToken=dacc8158b7ac4d468166ca3905b4d85c_NORMAL_60e49d77742ffb3e8188a552a5c05f52&signHistoryId=dacc8158b7ac4d468166ca3905b4d85c&fromType=scanRollCall 类型: QRCODE
            // 从消息中提取出url,然后访问


            // if (event.data.includes("https://mlearning.sjtu.edu.cn")) {
            //     // 使用正则表达式提取URL
            //     const urlRegex = /(https:\/\/mlearning\.sjtu\.edu\.cn\/[^\s]+)/;
            //     const match = event.data.match(urlRegex);
                
            //     if (match && match[0]) {
            //         const url = match[0];  // 提取的URL
            //         console.log("url: ", url);
                    
            //         // 正确访问URL（直接在新的窗口打开）



                    
            //         // 向消息中添加返回的URL
            //         messages.append(`return url: ${url}`);
            //         messages.append(`<li>url given back</li>`);
            //     } else {
            //         console.log("没有找到匹配的URL");
            //     }
            // }


            if (event.data.includes("https://mlearning.sjtu.edu.cn")) {
                // 使用正则表达式提取URL
                const urlRegex = /(https:\/\/mlearning\.sjtu\.edu\.cn\/[^\s]+)/;
                const match = event.data.match(urlRegex);
                
                if (match && match[0]) {
                    const url = match[0];  // 提取的URL
                    console.log("提取的URL: ", url);
                    
                    try {
                        // 解析原始URL
                        const originalUrl = new URL(url);
                        const params = new URLSearchParams(originalUrl.search);
                        
                        // 提取必要的查询参数
                        const courseCode = params.get('courseCode');
                        const rollCallToken = params.get('rollCallToken');
                        const signHistoryId = params.get('signHistoryId');
                        const fromType = params.get('fromType');
                        
                        // 检查所有必要参数是否存在
                        if (courseCode && rollCallToken && signHistoryId && fromType) {
                            // 获取当前时间戳，用于参数 t
                            const timestamp = Date.now();
                            
                            // 构建新的URL
                            const newUrl = `https://mlearning.sjtu.edu.cn/lms/mobile/?t=${timestamp}#/pages/course/CourseDetailPage?courseCode=${encodeURIComponent(courseCode)}&rollCallToken=${encodeURIComponent(rollCallToken)}&fromType=${encodeURIComponent(fromType)}&signHistoryId=${encodeURIComponent(signHistoryId)}`;
                            
                            console.log("重定向到新的URL: ", newUrl);
                            
                            // 在当前窗口重定向到新的URL
                            window.location.href = newUrl;
                            
                            // 如果希望在新窗口打开，可以使用以下代码：
                            window.open(newUrl, '_blank');
                        } else {
                            console.error("缺少必要的查询参数，无法重定向。");
                        }
                    } catch (error) {
                        console.error("解析URL时出错: ", error);
                    }
                } else {
                    console.error("未能提取到有效的URL。");
                }
            }
            
            
            
        }
    });

    // 绑定 stop-monitor 按钮事件
    data.html.find("#stop-monitor").click(function () {
        console.log("绑定成功：stop-monitor");
        // 这里可以添加实际的停止监测逻辑
        data.socket.send(`stop_monitor:${data.url}`);
        // debug,添加到messages列表
        const messages = data.html.find("#messages");
        messages.append(`<li>stop-monitor clicked</li>`);
    });

    return data.html;
}

function AddKey(key) {
    const data = {};
    data.html = $(`
        <div class="panel">
            <div class="panel-heading">
                <span class="name bold">${key}</span>
                <img src="img/copy.png" class="icon copy" id="copy" title="${i18n.copy}"/>
            </div>
            <div class="url hide">
                Hex: ${base64ToHex(key)}
            </div>
        </div>`);
    data.html.find('.panel-heading').click(function () {
        data.html.find(".url").toggle();
    });
    data.html.find('.copy').click(function () {
        navigator.clipboard.writeText(key);
        Tips(i18n.copiedToClipboard);
        return false;
    });
    return data.html;
}

/********************绑定事件********************/
// 一些需要等待G变量加载完整的操作
const interval = setInterval(function () {
    if (!G.initSyncComplete || !G.initLocalComplete || !G.tabId) { return; }
    clearInterval(interval);

    // 弹出模式 修改G.tabID为参数设定 设置css
    if (isPopup) {
        G.tabId = _tabId;
        $("body").css("width", "100%"); // body 宽度100%
        $("#popup").hide(); // 隐藏弹出按钮
        $("#more").hide();  // 隐藏更多功能按钮
        $("#down").append($("#features button")).css("justify-content", "center");  // 把更多功能内按钮移动到底部
        $("#down button").css("margin-left", "5px");    // 按钮间隔
        $("#currentPage").show();
    } else if (G.popup) {
        $("#popup").click();    // 默认弹出模式
    }

    // 获取页面DOM
    chrome.tabs.sendMessage(G.tabId, { Message: "getPage" }, { frameId: 0 }, function (result) {
        if (chrome.runtime.lastError) { return; }
        pageDOM = new DOMParser().parseFromString(result, 'text/html');
    });
    // 填充数据
    chrome.runtime.sendMessage(chrome.runtime.id, { Message: "getData", tabId: G.tabId }, function (data) {
        if (!data || data === "OK") {
            $tips.html(i18n.noData);
            $tips.attr("data-i18n", "noData");
            return;
        }
        currentCount = data.length;
        if (currentCount >= 500 && confirm(i18n("confirmLoading", [currentCount]))) {
            $mediaList.append($current);
            return;
        }
        for (let key = 0; key < currentCount; key++) {
            $current.append(AddMedia(data[key]));
        }
        $mediaList.append($current);
    });
    // 监听资源数据
    chrome.runtime.onMessage.addListener(function (MediaData, sender, sendResponse) {
        if (MediaData.Message) { return; }
        const html = AddMedia(MediaData, MediaData.tabId == G.tabId);
        if (MediaData.tabId == G.tabId) {
            !currentCount && $mediaList.append($current);
            currentCount++;
            $current.append(html);
        } else if (allCount) {
            allCount++;
            $all.append(html);
        }
        sendResponse("OK");
    });
    // 获取模拟手机 自动下载 捕获 状态

    // 上一次设定的倍数
    $("#playbackRate").val(G.playbackRate);

    $(`<style>${G.css}</style>`).appendTo("head");

    updateDownHeight();
    const observer = new MutationObserver(updateDownHeight);
    observer.observe($down[0], { childList: true, subtree: true, attributes: true });

    // 记忆弹出窗口的大小
    (isPopup && !G.isFirefox) && chrome.windows.onBoundsChanged.addListener(function (window) {
        chrome.storage.sync.set({
            popupHeight: window.height,
            popupWidth: window.width,
            popupTop: window.top,
            popupLeft: window.left,
        });
        updateDownHeight();
    });

    // 疑似密钥
    chrome.webNavigation.getAllFrames({ tabId: G.tabId }, function (frames) {
        if (!frames) { return; }
        for (let frame of frames) {
            chrome.tabs.sendMessage(G.tabId, { Message: "getKey" }, { frameId: frame.frameId }, function (result) {
                if (chrome.runtime.lastError || !result || result.length == 0) { return; }
                $("#maybeKeyTab").show();
                for (let key of result) {
                    $maybeKey.append(AddKey(key));
                }
                $("#maybeKey").append($maybeKey);
            });
        }
    });
    // 监听密钥
    chrome.runtime.onMessage.addListener(function (data, sender, sendResponse) {
        if (!data.Message || !data.data || data.Message != "popupAddKey") { return; }
        $("#maybeKeyTab").show();
        chrome.tabs.query({}, function (tabs) {
            let tabId = -1;
            for (let item of tabs) {
                if (item.url == data.url) {
                    tabId = item.id;
                    break;
                }
            }
            if (tabId == -1 || tabId == G.tabId) {
                $maybeKey.append(AddKey(data.data));
            }
            !$("#maybeKey .panel").length && $("#maybeKey").append($maybeKey);
        });
    });
}, 0);
/********************绑定事件END********************/

/* 格式判断 */
const isMediaExt = (ext) => ['ogg', 'ogv', 'mp4', 'webm', 'mp3', 'wav', 'm4a', '3gp', 'mpeg', 'mov', 'm4s', 'aac'].includes(ext);
function isPlay(data) {
    if (G.Player && !isJSON(data) && !isPicture(data)) { return true; }
    const typeArray = ['video/ogg', 'video/mp4', 'video/webm', 'audio/ogg', 'audio/mp3', 'audio/wav', 'audio/m4a', 'video/3gp', 'video/mpeg', 'video/mov'];
    return isMediaExt(data.ext) || typeArray.includes(data.type) || isM3U8(data);
}
function isM3U8(data) {
    return (data.ext == "m3u8" ||
        data.ext == "m3u" ||
        data.type == "application/vnd.apple.mpegurl" ||
        data.type == "application/x-mpegurl" ||
        data.type == "application/mpegurl" ||
        data.type == "application/octet-stream-m3u8"
    )
}
function isMPD(data) {
    return (data.ext == "mpd" ||
        data.type == "application/dash+xml"
    )
}
function isJSON(data) {
    return (data.ext == "json" ||
        data.type == "application/json" ||
        data.type == "text/json"
    )
}
function isPicture(data) {
    if (data.type && data.type.split("/")[0] == "image") {
        return true;
    }
    return (data.ext == "jpg" ||
        data.ext == "png" ||
        data.ext == "jpeg" ||
        data.ext == "bmp" ||
        data.ext == "gif" ||
        data.ext == "webp"
    )
}