var test = [];
angular.module("listNews", []);
angular.module("listNews").controller("newsControl", function ($scope) {
	$scope.title = "Lista de Notícias";
	$scope.news = [];
	$scope.insert = 'true';
	var getNews = function () {
		$.ajax({
			url: '/marvel_guide/backcall/getNews/',
			type: "GET",
			data: {},
			enctype: 'multipart/form-data',
			success:function(wRet){
				var ret = JSON.parse(wRet);
				$scope.news = ret;
				console.log($scope.news);
			},
			error: function (error) {
				return error;
			}
		});
	}
	$scope.insertNews = function (new_new) {
		$.ajax({
			url: '/marvel_guide/backcall/insert_news/',
			type: "POST",
			data: {'data' : new_new, 'insert' : $scope.insert},
			enctype: 'multipart/form-data',
			success:function(wRet){
				getNews();
			},
			error: function (error) {
				return error;
			}
		});
		delete $scope.new_new;
	};
	$scope.removeNews = function (news) {
		var notRemove = news.filter(function (new_new) {
			if (!new_new.sel) return new_new;
		});
		var ids = [];
		for (i in notRemove) ids.push(notRemove[i]['id']);
		$.ajax({
			url: '/marvel_guide/backcall/delete_news/',
			type: "POST",
			data: {'data' : ids},
			enctype: 'multipart/form-data',
			success:function(wRet){
				getNews();
			},
			error: function (error) {
				return error;
			}
		});
	}
	$scope.editNew = function (wId, news) {
		var aux = news.filter(function (new_new) {
			if (new_new.id == wId) return new_new;
		});
		$scope.new_new = aux[0];
		$scope.insert = wId;
	}
	$scope.cancelEdit = function cancelEdit() {
		$scope.insert = 'true';
		delete $scope.new_new;
	}
	getNews();
});