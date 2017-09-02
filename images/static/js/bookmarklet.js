(function () {
    var jquery_version = '2.1.4';
    var site_url = 'http://127.0.0.1:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;
    var min_height  =100;
    
    function bookmarklet(msg) {
        //载入css
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random() * 999999999999999)
        });
        jQuery('head').append(css);

        //载入HTML
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html); // 把div块加载到body标签
            //关闭事件
            jQuery('#bookmarklet #close').click(function () {
        jQuery('#bookmarklet').remove() //点击关闭直接移除整个块
            });

        // 找到图片并展示图片
        jQuery.each(jQuery('img[src$="jpg"]'), function (index, image) {
            if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height)
            {
                image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append('<a href="#"><img src="' + image_url + '"/></a>');

            }
        });

        // 用户点击图片弹出添加链接
        jQuery('#bookmarklet .images a').click(function (e) {
            selected_image = jQuery(this).children('img').attr('src');
            //隐藏 bookmarklet块
            jQuery('#bookmarklet').hide();
            //打开窗口提交新建图片
            window.open(site_url + 'images/create/?url='
                + encodeURIComponent(selected_image)
                + '&title='
                + encodeURIComponent(jQuery('title').text()),
                '_blank');
        });
    };

        if (typeof window.jQuery != 'undefined') {
            bookmarklet(); // 如果jQuery被加载了 ，调用函数
        } else {
            var conflict = typeof window.$ != 'undefined';
            var script = document.createElement('script'); //创建<script>标签
            script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' +
                jquery_version + '/jquery.min.js');
            //增加属性 调用谷歌jquery
            document.getElementsByTagName('head')[0].appendChild(script);
            //找到head标签在里面添加script
            var attempts = 15;
            (function () {
                if (typeof window.jQuery == 'undefined') {
                    if (--attempts > 0) {
                        window.setTimeout(arguments.callee, 250)
                    } else {
                        alert("An error ocurred while loading jQuery")
                    } //变量自减，如果到0，弹出错误，加载失败
                } else {
                    bookmarklet();
                }
            })();
        }
})();

