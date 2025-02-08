// 追加0
function appendZero(date) {
    return parseInt(date) < 10 ? `0${date}` : date;
}
// 秒转换成时间
function secToTime(sec) {
    let hour = (sec / 3600) | 0;
    let min = ((sec % 3600) / 60) | 0;
    sec = (sec % 60) | 0;
    let time = hour > 0 ? hour + ":" : "";
    time += min.toString().padStart(2, '0') + ":";
    time += sec.toString().padStart(2, '0');
    return time;
}
// 字节转换成大小
function byteToSize(byte) {
    if (!byte || byte < 1024) { return 0; }
    if (byte < 1024 * 1024) {
        return (byte / 1024).toFixed(1) + "KB";
    } else if (byte < 1024 * 1024 * 1024) {
        return (byte / 1024 / 1024).toFixed(1) + "MB";
    } else {
        return (byte / 1024 / 1024 / 1024).toFixed(1) + "GB";
    }
}
// 判断是否为空
function isEmpty(obj) {
    return (typeof obj == "undefined" ||
        obj == null ||
        obj == "" ||
        obj == " ")
}
