describe("Fotuto filters", function () {

	beforeEach(module('fotuto'));

	describe("getItem Filter", function () {

		it("Should has the getItem filter", inject(function ($filter) {
			expect($filter('getItem')).not.toBeNull();
		}));

		it("Should return undefined if list is empty", inject(function (getItemFilter){
			var vars = [];
			expect(getItemFilter(vars, 'other-var')).toBeUndefined();
		}));

		it("Should return the Item", inject(function (getItemFilter) {
			var some_var = {'slug': 'some-var', 'name': 'Some Var'};
			var other_var = {'slug': 'other-var', 'name': 'Other Var'};
			var vars = [some_var, other_var];

			expect(getItemFilter(vars, 'other-var')).toEqual(other_var);
			expect(getItemFilter(vars, 'non-exist')).toBeUndefined();
			expect(getItemFilter(vars, 'some-var')).toEqual(some_var);
		}));

		it("Should return the Object by a property", inject(function (getItemFilter) {
			var some_var = {'slug': 'some-var', 'name': 'Some Var'};
			var other_var = {'slug': 'other-var', 'name': 'Other Var'};
			var vars = [some_var, other_var];

			expect(getItemFilter(vars, {'name': "Some Var"})).toEqual(some_var);
			expect(getItemFilter(vars, {'name': "Some"})).toBeUndefined();
			expect(getItemFilter(vars, {'slug': 'other-var'})).toEqual(other_var);
		}));

		it("Should return the first Object by a property with the startswith filter", inject(function (getItemFilter) {
			var some_var = {'slug': 'some-var', 'name': 'Some Var'};
			var other_var = {'slug': 'other-var', 'name': 'Some Var 2'};
			var vars = [some_var, other_var];

			expect(getItemFilter(vars, {'name__startswith': "Some V"})).toEqual(some_var);
			expect(getItemFilter(vars, {'name__startswith': "Oter"})).toBeUndefined();
			expect(getItemFilter(vars, {'slug__startswith': 'other-'})).toEqual(other_var);
		}));
	});

	describe("contains Filter", function () {

		it("Should has the contains filter", inject(function ($filter) {
			expect($filter('contains')).not.toBeNull();
		}));

		it("Should return true if a number exist in array", inject(function (containsFilter) {
			var test_array = [1, 2, 3, 4];
			expect(containsFilter(test_array, 1)).toBeTruthy();
			expect(containsFilter(test_array, 5)).toBeFalsy();
		}));

		it("Should return true if a string exist in array", inject(function (containsFilter) {
			var test_array = ["A", "B", "C"];
			expect(containsFilter(test_array, "A")).toBeTruthy();
			expect(containsFilter(test_array, "Z")).toBeFalsy();
		}));
	});

});