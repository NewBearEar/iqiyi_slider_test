// 已删除关键 js, RSA 加密, 请自行补全

function RSAEncrypt(text) {
    var encrypter = new zc();
    var publicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfyy01w1BXvMX8hc0ooyaCcXv2A0fsqDjcEXZ8AQJSHU00iG9YoYyLwmS0G9eE+dEFomOI2a+mrh9JYpw2Y26oGFZFA8Dtly5Go4nXeFT/pEeSwWINcXQ5Y9WCMTkQ+RN5WJ0UPvWt+soqP3Z5FJdMJTWA4lwIyoN3c4d9dWcpkQIDAQAB";
    encrypter.setPublicKey(publicKey);
    return encrypter.encrypt(a(text))
}

r.biFromHex = function(e) {
    for (var i = new g, t = e.length, o = t, n = 0; o > 0; o -= 4,
    ++n)
        i.digits[n] = r.hexToDigit(e.substr(Math.max(o - 4, 0), Math.min(o, 4)));
    return i
}


var q = function(i, t, o) {
    var n = r;
    this.e = n.biFromHex(i),
    this.d = n.biFromHex(t),
    this.m = n.biFromHex(o),
    this.chunkSize = 2 * n.biHighIndex(this.m),
    this.radix = 16,
    this.barrett = new e.BarrettMu(this.m)
};
r.getKeyPair = function(e, i, t) {
    return new q(e,i,t)
}