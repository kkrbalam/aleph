aleph.controller('EntitiesMergeCtrl', ['$scope', '$location', '$q', '$http', '$uibModalInstance', 'entities',
    function($scope, $location, $q, $http, $uibModalInstance, entities) {

  $scope.entities = entities.sort(function(a, b) {
    return (b.doc_count || 0) - (a.doc_count || 0);
  });
  $scope.primary = $scope.entities[0].id;

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };

  $scope.confirm = function() {
    var merges = [];
    for (var i in entities) {
      var id = entities[i].id;
      if (id != $scope.primary) {
        var url = '/api/1/entities/' +   $scope.primary + '/merge/' + id;
        merges.push($http.delete(url));  
      }
    }
    $q.all(merges).then(function() {
      $uibModalInstance.close($scope.primary);
    }, function(err) {
      console.log('Delete error', err);
      $uibModalInstance.close($scope.primary);
    });
  };

}]);