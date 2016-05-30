/**
 * AngularJS filter to convert a number in positive
 */
fotuto.filter('abs', function () {
	return function (num) {
		return Math.abs(num);
	}
});

/**
 * Filter to get an element from a list by its property value
 *
 * Usage examples:
 *
 *     vars | getItem:'some-slug'
 *     vars | getItem:{id: 1}
 *     vars | getItem:{'name__startswith': "Door Sen"}
 *
 * @param (array) list: The list to look for an item
 * @param (string|object) param: The value to look for. If `param` is just a string it will search by the `slug` 
 *    property. Also the parameter could be an object in the format `{'<PROPERTY_NAME>[__startswith]' : '<VALUE>'}`. By 
 *    adding `__startswith` tail to the property name it will search the value of the property that starts with the 
 *    *<VALUE>*.
 *
 */
fotuto.filter('getItem',
	function () {
		return function (list, param) {
			// TODO: Refactor this function

			function filter_function(item) {
				var key, value;
				if (typeof param == 'object') {
					key = Object.keys(param)[0];
					var key_arr = key.split('__');
					if (key_arr.length == 2 && key_arr[1] == 'startswith') {
						return item[key_arr[0]].indexOf(param[key]) == 0;
					} else {
						return item[key_arr[0]] == param[key];
					}
				}
				return item.slug == param;
			}

			return list.filter(filter_function)[0];
		}
	}
);

/**
 * Filter to check in an element exist in an array
 */
fotuto.filter('contains', function () {
	return function (array, needle) {
		return array.indexOf(needle) >= 0;
	};
});

fotuto.filter('unsafe', function($sce) { return $sce.trustAsHtml; });